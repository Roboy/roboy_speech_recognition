import speech_recognition as sr
import socket
import threading
import numpy as np
# import pyaudio
import pdb
import io
import time

# import asyncio
class Odas(sr.AudioSource):

    def __init__(self, port, host='0.0.0.0', channel=0, chunk_size=1024, sample_rate=16000):
        # self.format = pyaudio.paInt16
        self.SAMPLE_WIDTH = 2#pyaudio.get_sample_size(self.format)  # size of each sample
        self.SAMPLE_RATE = sample_rate  # sampling rate in Hertz
        self.CHUNK = chunk_size

        self.audio = None
        self.stream = None
        self.pyaudio_stream = None

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
        print("Odas connected")
        self.record = True


        d = threading.Thread(target=self.write_to_stream)
        self.lock = threading.RLock()
        d.setDaemon(True)
        d.start()

        self.stream = Odas.BytesLoop()
        self.channels = [sr.AudioSource]


    def write_to_stream(self):#, reader, writer):
        print("Started deamon")
        while True:
            data = self.conn.recv(4*self.CHUNK)
            # self.lock.acquire()
            # print("got lock")
            if self.record:
                # print("oh")

                try:
                    data = np.frombuffer(data, dtype=np.int16)
                    # if np.count_nonzero(data) > 0:
                        # pdb.set_trace()
                        # print("this is not a zero")
                        # energy = audioop.rms(data, self.SAMPLE_WIDTH)
                        # if energy > 0:
                        #     print ("energy is not zero")
                    # for i in range(4):
                    #     data = data[i:4].tobytes()
                    #     energy = audioop.rms(data, source.SAMPLE_WIDTH)
                    #     if energy >0:
                    #         print("in channel possitive energy " + str(i))
                    data = data[0::4].tobytes()
                    self.stream.write(data)
                    # print("yay")
                except:
                    pass
            # self.lock.release()
                # print("released lock")

    def __enter__(self):
        # assert self.stream is None, "This audio source is already inside a context manager"
        # self.audio = pyaudio.PyAudio()
        try:
            # pdb.set_trace()
            # self.lock.acquire()
            self.record = True
            # self.lock.release()

            # self.pyaudio_stream = self.audio.open(
            #     channels=1, format=self.format,
            #     rate=self.SAMPLE_RATE, frames_per_buffer=self.CHUNK, output=True, input=True
            # )
            # self.stream = Odas.MicrophoneStream(self.pyaudio_stream)


        except Exception:
            print("exception in enter")
            # self.audio.terminate()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
            # self.lock.acquire()
            self.stream = None
            self.record = False
            # self.lock.release()
            # self.audio.terminate()

    class BytesLoop:
        def __init__(self, s=b''):
            self.buffer = s
            self.lock = threading.RLock()

        def read(self, n=-1):
            # print("read %i"%n)
            while len(self.buffer) < n:
                pass
            self.lock.acquire()

            chunk = self.buffer[:n]
            self.buffer = self.buffer[n:]
            self.lock.release()
            return chunk

        def write(self, s):
            # print("write %i"%len(s))
            self.lock.acquire()
            self.buffer += s
            self.lock.release()

    class MicrophoneStream(object):
        def __init__(self, pyaudio_stream):
            self.pyaudio_stream = pyaudio_stream

        def read(self, size):
            return self.pyaudio_stream.read(size)#, exception_on_overflow=False)

        def close(self):
            try:
                # sometimes, if the stream isn't stopped, closing the stream throws an exception
                if not self.pyaudio_stream.is_stopped():
                    self.pyaudio_stream.stop_stream()
            finally:
                self.pyaudio_stream.close()


r = sr.Recognizer()

# loop = asyncio.get_event_loop()

with Odas(10002) as source:
# with sr.AudioFile('/home/missxa/workspace/Roboy/src/roboy_speech_recognition/roboy_speech_recognition/scripts/speech_recognition/examples/english.wav') as source:
    # coro = asyncio.start_server(source.write_to_stream, host, port, loop=loop)
    # server = loop.run_until_complete(coro)
    # time.sleep(3)
    # while True:
    #     print(len(source.stream.buffer))
    audio = r.listen(source)

BING_KEY = "e91e7a4512aa48b3b53b36b56bd1feb7"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
try:
    print(r.recognize_bing(audio, key=BING_KEY))
except sr.UnknownValueError:
    print("Microsoft Bing Voice Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))


# loop.run_forever()
# print("doing some async stuff")
# o = Odas(10002)
# o = o.__enter__()
# time.sleep(4)
# pdb.set_trace()
# o.__exit__(None, None, None)
