from . import audio
from flask import (request,
                   jsonify,
                   make_response,
                   current_app,
                   send_from_directory,
                   abort)
from werkzeug.utils import secure_filename
from .audio_bass_boost import export_bass_boosted

from app import rq

ALLOWED_EXTENSIONS = set(['mp3', 'aac', 'wav', 'flac'])


def allowed_file(filename):
    return ('.' in filename
            and
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


@audio.route("/", methods=['GET', 'POST'])
def index():
    # validate that the incoming request body is JSON
    if request.is_json:
        # parse the JSON request body into python dictionary
        req = request.get_json()
        # make response body
        response_body = {
            "success": True,
            'message': 'JSON Recieved',
            'sender':   req.get('name')
        }
        # make a JSON response with status code OK
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(
            jsonify({"success": False,
                     "message": "Request body must be JSON"}), 400)


@audio.route("/bass-boost", methods=['GET', 'POST'])
def bass_boost():
    if request.method == 'POST':
        default_queue = rq.get_queue()
        default_queue.empty()
        if 'audio' not in request.files:
            resp = make_response(
                jsonify({"success": False,
                         'message': 'No file part in the request'}), 400)
            return resp
        audio_file = request.files['audio']
        if audio_file.filename == '':
            resp = make_response(
                jsonify({"success": False,
                         'message': 'No file selected for uploading'}), 400)
            return resp
        if audio_file and allowed_file(audio_file.filename):
            filename = secure_filename(audio_file.filename)
            upload_dir = current_app.config['AUDIO_UPLOADS']
            audio_file.save(upload_dir.joinpath(filename))

            job = export_bass_boosted.queue(upload_dir, filename)

            resp = make_response(
                jsonify({"success": True,
                         'message': 'File successfully uploaded'}), 201)
            resp.set_cookie('FILENAME', filename)
            resp.set_cookie('JOB_ID', job.id)
            return resp
        else:
            resp = make_response(
                jsonify(
                    {"success": False,
                     'message': 'Allowed file types are mp3, aac, wav, flac'}),
                400)
            return resp
    if request.method == 'GET':

        print('cookie job id: ', request.cookies.get('JOB_ID'))
        default_queue = rq.get_queue()
        print('list of job IDs from the queue: ', default_queue.jobs)
        job = default_queue.fetch_job(request.cookies.get('JOB_ID'))
        print('Status: ', job.get_status())

        if job.is_finished:
            try:
                export_dir = current_app.config["AUDIO_EXPORTS"]
                file_name = request.cookies.get(
                    'FILENAME').replace(".mp3", "-export.mp3")
                return send_from_directory(export_dir,
                                           filename=file_name,
                                           as_attachment=True)

            except FileNotFoundError:
                abort(404)

        else:
            resp = make_response(jsonify(
                {"success": True,
                 'message': 'Processing'}), 200)
            return resp
