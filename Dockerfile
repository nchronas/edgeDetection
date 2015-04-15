FROM resin/rpi-raspbian:latest
RUN apt-get update -y && apt-get install -y \
python python-pip python-dev python-dbus python-flask \
dropbear \
nano \
&& apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install RPi.GPIO
COPY . /app
CMD ["bash", "/app/start.sh"]
