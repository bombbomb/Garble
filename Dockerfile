FROM ubuntu
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev
RUN apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 libav-tools

COPY ffmpeg /bin
RUN chmod 777 /bin/ffmpeg
COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt
COPY . app
EXPOSE 5000:5000
ENTRYPOINT ["python"]
CMD ["app/app.py"]