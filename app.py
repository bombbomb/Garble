from flask import Flask
import speech_recognition as sr
from ffmpy import FFmpeg
from os import path
import uuid

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/transcribe")
def transcribe():

    audio_path = path.join(path.dirname(path.realpath(__file__)), str(uuid.uuid4()) + '.flac')

    video_input_path = path.join(path.dirname(path.realpath(__file__)), 'example.mp4')

    ff = FFmpeg(
        inputs={video_input_path: None},
        outputs={audio_path: ['-c:a', 'flac']}
    )

    print(ff.cmd)

    ff.run()

    print('Made FLAC: ' + audio_path)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)

    try:
        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
