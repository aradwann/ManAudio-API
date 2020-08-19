import pathlib
from . import audio
from flask import (request,
                   jsonify,
                   make_response,
                   current_app,
                   send_file,
                   send_from_directory,
                   safe_join,
                   abort)
from werkzeug.utils import secure_filename


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


@audio.route("/upload", methods=["POST"])
def upload_audio():
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
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(
            {'message': 'Allowed file types are mp3, aac, wav, flac'})
        resp.status_code = 400
        return resp


@audio.route('/download/<filename>')
def download_audio(filename):
    try:
        return send_from_directory(current_app.config["AUDIO_UPLOADS"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
