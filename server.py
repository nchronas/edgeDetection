import time
import RPi.GPIO as GPIO
import socket
import SocketServer
import SimpleHTTPServer
import sys
import os
from time import sleep
from urlparse import urlparse, parse_qs


PORT = 80
logList = []
sampleSize = 1024
log = False


def my_callback(channel):
    global logList, log, sampleSize
    if log == True :
        timelog = time.time() - logStart
        logList.append( [ (channel, GPIO.input(channel), timelog)] 
        if len(logList) > sampleSize:
            log = False
    #print "event", channel, GPIO.input(channel), timelog 

print "Hello from Resin"

GPIO.setmode(GPIO.BOARD)

GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


GPIO.add_event_detect(40, GPIO.RISING, callback=my_callback)  # add rising edge detection on a channel

    
class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        print self.path  
        print 'server request'

        if self.path[0:6]=='/start':
            global log, logStart, logList
            print "started logging"
            logStart = time.time() 
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            logList = []
            log = True
            return

        elif self.path[0:5]=='/stop':
            global log
            print "stoppedlogging"
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            log = False
            return 

        elif self.path[0:7]=='/status':
            print "logging status"
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(log)
            return 

        elif self.path[0:4]=='/log':
			global logList
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            for row in logList:
                self.wfile.write(row)
            return 

        elif self.path[0:7]=='/sample':
            global sampleSize
            test=parse_qs(urlparse(self.path).query)
            print test, "get values"
            if test  :
                sampleSize=test['size']
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(''' ''')
            return 

        else:
        #serve files, and directory listings by following self.path from
        #current working directory
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


httpd = SocketServer.ThreadingTCPServer(('', PORT),CustomHandler)
 
print "serving at port", PORT
httpd.serve_forever()
