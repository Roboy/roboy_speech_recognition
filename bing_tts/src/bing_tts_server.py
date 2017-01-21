#!/usr/bin/env python

import rospy
import os
import sys
import pyaudio

import ipdb 

abs_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(abs_path, "..", "..", "common"))

from bing_voice import *
from  bing_tts.srv import *

BING_KEY = ''

def handle_tts(req):
    try:
        bing.synthesize(req.text)
        return True
    except Exception, e:
        return False
        print "Unable to synthesize text. The following error occured: ", e

def tts_server():
    rospy.init_node('TextToSay')
    s = rospy.Service('TextToSay', TextToSay, handle_tts)

    global bing 
    bing = BingVoice(BING_KEY)
    
    print "Ready to synthesize speech."
    rospy.spin()

if __name__ == '__main__':
	tts_server()
