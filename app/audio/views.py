import pathlib
from . import audio
from flask import (request,
                   jsonify,
                   make_response,
                   current_app,
                   send_file,
                   send_from_directory,
                   safe_join,
                   abort,
                   url_for,
                   redirect,
                   session)
from werkzeug.utils import secure_filename
from .audio_bass_boost import export_bass_boosted

from redis import Redis
from rq import Queue, get_current_job

redis_conn = Redis()
q = Queue(connection=redis_conn)

ALLOWED_EXTENSIONS = set(['mp3', 'aac', 'wav', 'flac'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@audio.route("/", methods=['GET', 'POST'])
def index():
    # validate that the incoming request body is JSON
    if request.is_json:
        # parse the JSON request body into python dictionary
        req = request.get_json()
        # make response body
        response_body = {
            'message': 'JSON Recieved',
            'sender':   req.get('name')
        }
        # make a JSON response with status code OK
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)


@audio.route("/bass-boost", methods=['GET', 'POST'])
def bass_boost():
    if request.method == 'POST':
        if 'audio' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['audio']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(current_app.config["AUDIO_UPLOADS"].joinpath(filename))
            job = q.enqueue(export_bass_boosted, args=(
                current_app.config['AUDIO_UPLOADS'], filename), job_id='my_audio_proc')
            # session['FILENAME'] = filename
            # session['JOB_ID'] = 'my_audio_proc'
            resp = jsonify({'message': 'File successfully uploaded'})
            resp.set_cookie('FILENAME', filename)
            resp.status_code = 201
            resp.set_cookie('FILENAME', filename)
            resp.set_cookie('JOB_ID', 'my_audio_proc')
            return resp
        else:
            resp = jsonify(
                {'message': 'Allowed file types are mp3, aac, wav, flac'})
            resp.status_code = 400
            return resp
    if request.method == 'GET':
        # try:

        job = q.fetch_job(request.cookies.get('JOB_ID'))
        print(request.cookies.get('FILENAME'))
        print(job.get_status())
        if job.get_status() != 'finished':
            resp = jsonify(
                {'message': 'Processing'})
            resp.status_code = 200
            return resp
        else:
            return send_from_directory(current_app.config["AUDIO_EXPORTS"], filename=request.cookies.get('FILENAME').replace(".mp3", "-export.mp3"), as_attachment=True)

        # except FileNotFoundError:
        #         abort(404)


