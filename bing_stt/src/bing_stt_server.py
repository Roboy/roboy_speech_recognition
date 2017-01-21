#!/usr/bin/env python

import rospy
from multiprocessing import Process, Queue

import ipdb 

from bing_stt_with_vad import stt_with_vad
from bing_voice import *
from  bing_stt.srv import *

BING_KEY = 'f03ec159eb2c4f1dafffebc5750037f2'

def stt_subprocess(q):
	q.put(stt_with_vad(bing))

def handle_stt(req):
	queue = Queue()
	p = Process(target = stt_subprocess, args = (queue,))
	p.start()
	p.join()
	return queue.get()

def stt_server():
    rospy.init_node('TextSpoken')
    s = rospy.Service('TextSpoken', TextSpoken, handle_stt)

    global bing 
    bing = BingVoice(BING_KEY)
    
    print "Ready to recognise speech."
    rospy.spin()

if __name__ == '__main__':
	stt_server()