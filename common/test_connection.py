key = 'f03ec159eb2c4f1dafffebc5750037f2'
###
#Copyright (c) Microsoft Corporation
#All rights reserved. 
#MIT License
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ""Software""), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###
# import http.client
import  urllib, json, ipdb
import pyaudio
import wave
import httplib
import io

class AudioFile:
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """ 
        self.wf = file#wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def close(self):
        """ Graceful shutdown """ 
        self.stream.close()
        self.p.terminate()




#Note: The way to get api key:
#Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
#Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0
apiKey = key

params = ""
headers = {"Ocp-Apim-Subscription-Key": apiKey}

#AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
AccessTokenHost = "api.cognitive.microsoft.com"
path = "/sts/v1.0/issueToken"

# Connect to server to get the Access Token
print ("Connect to server to get the Access Token")
conn = httplib.HTTPSConnection(AccessTokenHost)
conn.request("POST", path, params, headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()

accesstoken = data.decode("UTF-8")
print ("Access Token: " + accesstoken)

body = "<speak version='1.0' xml:lang='en-us'><voice xml:lang='en-us' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>This is a demo to call microsoft text to speech service in python.</voice></speak>"

headers = {"Content-type": "application/ssml+xml", 
			"X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm", 
			"Authorization": "Bearer " + accesstoken, 
			"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
			"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960", 
			"User-Agent": "TTSForPython"}
			
#Connect to server to synthesize the wave
print ("\nConnect to server to synthesize the wave")
conn = httplib.HTTPSConnection("speech.platform.bing.com")
conn.request("POST", "/synthesize", body, headers)
response = conn.getresponse()
print(response.status, response.reason)

def to_wav(raw_data):
    # generate the WAV file contents
    with io.BytesIO() as wav_file:
        wav_writer = wave.open(wav_file, "wb")
        try:  # note that we can't use context manager, since that was only added in Python 3.4
            wav_writer.setframerate(16000)
            wav_writer.setsampwidth(2)
            wav_writer.setnchannels(1)
            wav_writer.writeframes(raw_data)
            wav_data = wav_file.getvalue()
        finally:  # make sure resources are cleaned up
            wav_writer.close()
    return wav_data

f = to_wav(data)
# Usage example for pyaudio
a = AudioFile(f)
a.play()
a.close()

print("The synthesized wave length: %d" %(len(data)))