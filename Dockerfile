FROM resin/rpi-raspbian:latest
RUN apt-get update -y
RUN apt-get install -y apt-utils
RUN apt-get install -y python python-pip python-dev python-dbus python-flask
RUN apt-get install -y dropbear
RUN pip install RPi.GPIO
COPY . /app
CMD ["bash", "/app/start.sh"]
