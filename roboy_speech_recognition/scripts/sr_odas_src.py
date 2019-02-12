import speech_recognition as sr
import socket
import threading
import numpy as np
import pdb
import io
import time
from monotonic import monotonic

class Odas(sr.AudioSource):
    class AudioSource(sr.AudioSource):
        def __init__(self, name, sample_rate, chunk_size=1024):
            self.SAMPLE_WIDTH = 2
            self.SAMPLE_RATE = sample_rate
            self.CHUNK = chunk_size
            self.stream = Odas.BytesLoop()
            self.record = False
            self.name = name

        def __enter__(self):
            # assert self.stream is None, "This audio source is already inside a context manager"
            self.record = True
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.stream = None
            self.record = False

    def __init__(self, port, host='0.0.0.0', sample_rate=16000, chunk_size=1024):
        # self.format = pyaudio.paInt16
        self.SAMPLE_WIDTH = 2#pyaudio.get_sample_size(self.format)  # size of each sample
        self.SAMPLE_RATE = sample_rate  # sampling rate in Hertz
        self.CHUNK = chunk_size
        self.CHANNELS = 4

        self.stream = Odas.BytesLoop()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
        print("Odas connected")

        d = threading.Thread(target=self.write_to_streams)
        self.lock = threading.RLock()
        d.setDaemon(True)
        d.start()

        self.channels = []
        for i in range(self.CHANNELS):
            self.channels.append(self.AudioSource(name="odas_%i"%i, \
                            sample_rate=sample_rate, chunk_size=chunk_size))

    def write_to_streams(self):
        print("Started odas deamon")
        while True:
            data = self.conn.recv(4*self.CHUNK)
            # if self.record:
            data = np.frombuffer(data, dtype=np.int16)
            #     self.stream.write(data[0::4].tobytes())
            for i in range(self.CHANNELS):
                if self.channels[i].record:
                    self.channels[i].stream.write(data[i::4].tobytes())

    def __enter__(self):
        # assert self.stream is None, "This audio source is already inside a context manager"
        self.record = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream = None
        self.record = False

    class BytesLoop:
        def __init__(self, s=b''):
            self.buffer = s
            self.lock = threading.RLock()

        def read(self, n=-1):
            # print("read %i"%n)
            while len(self.buffer) < n:
                pass
            # self.lock.acquire()

            chunk = self.buffer[:n]
            self.buffer = self.buffer[n:]
            # self.lock.release()
            return chunk

        def write(self, s):
            # print("write %i"%len(s))
            # self.lock.acquire()
            self.buffer += s
            # self.lock.release()




BING_KEY = ""  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings

r = sr.Recognizer()
o = Odas(port=10002, chunk_size=2048)
def listener(source):
    with source as source:
        audio = r.listen(source=source)
        try:
            print("%s: "%source.name + r.recognize_bing(audio, key=BING_KEY))
        except sr.UnknownValueError:
            print("Microsoft Bing Voice Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

listeners = []
for i in range(4):
    listeners.append(threading.Thread(target=listener, args = (o.channels[i],)))

for l in listeners:
    l.start()
