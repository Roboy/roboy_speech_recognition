# BingROS
ROS nodes for Bing Speech API services

## Dependencies
- `monotonic`
- `pyaudio`
- `webrtcvad`

```
sudo apt install python-pyaudio
pip install -r requirements.txt
```

## Usage
In order to synthesize text call the following service which will return the success status:
```
rosservice call /TextToSay "text: 'hello! im roboy'"
```

To recognize speech use the following service which will return the recognized string: 
```
rosservice call /TextSpoken 
```

To use Cerevoice TTS call (corresponding NodeRed socket has to be running):
```
rosservice call /CerevoiceTTS "text: 'hello! im roboy'"
```
