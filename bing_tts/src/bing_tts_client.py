#!/usr/bin/env python

import sys
import rospy
import ipdb

from bing_stt.srv import *

def stt_client():
	rospy.wait_for_service("TextToSay")
	try:
		stt = rospy.ServiceProxy('TextToSay', TextToSay)
		resp = stt("testing Ro boy's voice")
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e

if __name__ == "__main__":
	stt_client()