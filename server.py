import time
import RPi.GPIO as GPIO
import socket
import SocketServer
import SimpleHTTPServer
import sys
import os
from time import sleep
from urlparse import urlparse, parse_qs


def my_callback(channel):
#    print('This is a edge event callback function!')
#    print('Edge detected on channel %s'%channel)
#    print('This is run in a different thread to your main program')

print "Hello from Resin"

GPIO.setmode(GPIO.BOARD)

GPIO.setup(40, GPIO.IN)

#GPIO.add_event_detect(40, GPIO.RISING, callback=my_callback)  # add rising edge detection on a channel


PORT = 80

log = False
    
class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        print self.path  
        print 'server request'

        if self.path[0:5]=='/start':
			global log
            print "started logging" 
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            log = True
            return

        else if self.path[0:5]=='/stop':
            global log
            print "stoppedlogging"
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            log = False
            return 

        else if self.path[0:7]=='/status':
            print "logging status"
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(log)
            return 

        else if self.path[0:4]=='/log':
            print "hello my friend" 
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(''' ''')
            return        
            
        else:
        #serve files, and directory listings by following self.path from
        #current working directory
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

