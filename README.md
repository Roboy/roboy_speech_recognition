# BingROS
ROS nodes for Bing Speech API services
Bing Speech API token is required.

## Dependencies

```
sudo apt install python-pyaudio
pip install -r requirements.txt
```

## Usage

Launch the node
```
roslaunch roboy_speech_recognition speech_recogniton.launch
```

To recognize speech use the following service which will return the recognized string: 
```
rosservice call /roboy/cognition/speech/recognition {}
```
