from flask import Flask
import speech_recognition as sr
from ffmpy import FFmpeg
from os import path
import uuid
from flask import request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/health-check")
def health():
    return "Hi"


@app.route("/transcribe")
def transcribe():

    audio_path = path.join(path.dirname(path.realpath(__file__)), str(uuid.uuid4()) + '.flac')

    requested_video_path = request.args.get('videoUrl')

    if requested_video_path is None:
        return "You must provide a 'videoUrl' parameter"

    print("Requested video path: " + requested_video_path)

    try:
        ff = FFmpeg(
            inputs={(requested_video_path): None},
            outputs={audio_path: ['-c:a', 'flac']}
        )

        print(ff.cmd)

        ff.run()

        print('Made FLAC: ' + audio_path)

    except Exception as e:
        print("FFmpeg error {0}".format(e))
        return "Error extracting audio "

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)

    transcription = '[Could not transcribe]'

    try:
        transcription = r.recognize_sphinx(audio)
        print("Sphinx thinks you said " + transcription)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    os.remove(audio_path)

    return transcription


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
