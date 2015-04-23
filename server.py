import time
import RPi.GPIO as GPIO
import sys
import os
from time import sleep
from gevent import monkey
monkey.patch_all()

from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, \
    close_room, disconnect

PORT = 80
logList = []
sampleSize = 1024
log = False


def my_callback(channel):
#    global logList, log, sampleSize
#    if log == True :
#        timelog = time.time() - logStart
#        logList.append( [ (channel, GPIO.input(channel), timelog)])
#        if len(logList) > sampleSize:
#            log = False
    print "event", channel, GPIO.input(channel), timelog 
    socketio.emit('my response',
                     {'data': 'Server generated event', 'count': count},
                     namespace='/test')

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, PORT)
thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

print "Hello from Resin"

GPIO.setmode(GPIO.BOARD)

GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(40, GPIO.RISING, callback=my_callback)  # add rising edge detection on a channel

    
# class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
#     def log_message(self, format, *args):
#         return

#     def do_GET(self):
#         print self.path  
#         print 'server request'

#         if self.path[0:6]=='/start':
#             global log, logStart, logList
#             print "started logging"
#             logStart = time.time() 
#             self.send_response(200)
#             self.send_header('Content-type','text/html')
#             self.end_headers()
#             logList = []
#             log = True
#             return

#         elif self.path[0:5]=='/stop':
#             global log
#             print "stoppedlogging"
#             self.send_response(200)
#             self.send_header('Content-type','text/html')
#             self.end_headers()
#             log = False
#             return 

#         elif self.path[0:7]=='/status':
#             print "logging status"
#             self.send_response(200)
#             self.send_header('Content-type','text/html')
#             self.end_headers()
#             self.wfile.write(log)
#             return 

#         elif self.path[0:4]=='/log':
#             global logList
#             self.send_response(200)
#             self.send_header('Content-type','text/html')
#             self.end_headers()
#             for row in logList:
#                 self.wfile.write(row)
#             return 

#         elif self.path[0:7]=='/sample':
#             global sampleSize
#             test=parse_qs(urlparse(self.path).query)
#             print test, "get values"
#             if test  :
#                 sampleSize=test['size']
#             self.send_response(200)
#             self.send_header('Content-type','text/html')
#             self.end_headers()
#             self.wfile.write(''' ''')
#             return 

#         else:
#         #serve files, and directory listings by following self.path from
#         #current working directory
#             SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


# httpd = SocketServer.ThreadingTCPServer(('', PORT),CustomHandler)
 
# print "serving at port", PORT
# httpd.serve_forever()
