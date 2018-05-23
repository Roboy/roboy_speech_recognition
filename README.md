# BingROS
ROS nodes for Bing Speech API services
Bing Speech API token is required.

## Dependencies
- `monotonic`
- `pyaudio`
- `webrtcvad`
- `roboy_communication_cognition`

```
sudo apt install python-pyaudio
pip install -r requirements.txt
```

## Usage
Insert your Bing key in `common/bing_voice.py` and `roboy_speech_recognition/scripts/stt_server.py`.

Launch the node
```
roslaunch roboy_speech_recognition speech_recogniton.launch
```

To recognize speech use the following service which will return the recognized string: 
```
rosservice call /roboy/cognition/speech/recognition {}
```
