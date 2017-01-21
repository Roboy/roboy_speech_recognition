# BingROS
ROS nodes for Bing Speech API services

## Dependencies
- `mototonic`
- `pyaudio`
- `webrtcvad`
- `urllib`, `urlib2`, `httplib`
- `rospy`

## Usage
In order to synthesize text call the following service which will return the success status:
```
rosservice call /TextToSay "hello! i'm roboy"
```

To recognize speech use the following service which will return the recognized string: 
```
rosservice call /TextSpoken 
```
