import json
from flask import current_app
from app.audio.audio_bass_boost import export_bass_boosted
from .gen_audio import sound_generation
from pydub import AudioSegment


def test_export_bass_boosted(client):
    """Test exporting bass boosted audio file with fake redis connection
     and fake worker which actually works on the main thread"""

    Output_file_name = current_app.config['AUDIO_UPLOADS'].joinpath('test.au')
    destin_path = current_app.config['AUDIO_UPLOADS'].joinpath('test.mp3')
    sound_generation(Output_file_name)
    # convert audio file to suppoted format to avoid decoding error
    sound = AudioSegment.from_file(Output_file_name)
    sound.export(destin_path, format="mp3")
    job = export_bass_boosted.queue(
        current_app.config['AUDIO_UPLOADS'], 'test.mp3')
    assert job.is_finished


'''
def test_get_bass_boost(client):
    """Test GET request to bass boost
     that is going to return a 404 error"""

    response = client.get(
        '/audio/bass-boost')
    data = json.loads(response.data.decode())
    assert not data['success']
    assert data['message'] == 'not_found'
    # assert data['data']['email'] == 'joe@gmail.com'
    # assert data['data']['admin'] == 'true' or 'false'
    assert response.status_code == 404
'''
