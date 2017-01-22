#!/usr/bin/env python

import rospy
import os
import sys
import socket

from  cerevoice_tts.srv import *

def handle_tts(req):
    try:
        text = "text:" + req.text
        connection.send(text)
        return True
    except Exception, e:
        print "Unable to synthesize text. The following error occured: ", e
        return False

def tts_server():
    rospy.init_node('CerevoiceTTS')
    s = rospy.Service('CerevoiceTTS', CerevoiceTTS, handle_tts)

    global connection
    TCP_IP = '10.177.254.114'
    TCP_PORT = 30000 
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((TCP_IP, TCP_PORT))

    print "Ready to synthesize speech using Cerevoice."
    rospy.spin()

if __name__ == '__main__':
	tts_server()
