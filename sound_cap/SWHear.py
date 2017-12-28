import pyaudio
import time
import numpy as np
import threading
from sound_cap.utils.logger import Logger

np.seterr(all='warn')
LOG = Logger()


def fourier_frequency(data, rate):
    """Given some data and rate, returns FFTfreq and FFT (half)."""
    # smoothed_data = data * np.hamming(len(data))
    fft = np.abs(np.fft.fft(data))
    freq = np.fft.fftfreq(len(fft), 1.0 / rate)
    return freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)]


class SWHear:
    """
    The SWHear class is provides access to continuously recorded
    (and mathematically processed) microphone data.

    Arguments:

        device - the number of the sound card input to use. Leave blank
        to automatically detect one.

        rate - sample rate to use. Defaults to something supported.

        updatesPerSecond - how fast to record new data. Note that smaller
        numbers allow more data to be accessed and therefore high
        frequencies to be analyzed if using a FFT later
    """

    def __init__(self, device=1, rate=None, refresh_rate=10):
        self.audio_rec = pyaudio.PyAudio()
        self.chunk_size = 4096
        self.refresh_rate = refresh_rate
        self.chunksRead = 0
        self.device = device
        self.rate = rate

    ### SYSTEM TESTS

    def valid_low_rate(self, device):
        """set the rate to the lowest supported audio rate."""
        for testrate in [44100]:
            if self.valid_test(device, testrate):
                return testrate
        print("SOMETHING'S WRONG! I can't figure out how to use DEV", device)
        return None

    def valid_test(self, device, rate=44100):
        """given a device ID and a rate, return TRUE/False if it's valid."""
        try:
            self.info = self.audio_rec.get_device_info_by_index(device)
            if not self.info["maxInputChannels"] > 0:
                return False
            stream = self.audio_rec.open(format=pyaudio.paInt16, channels=1,
                                         input_device_index=device, frames_per_buffer=self.chunk_size,
                                         rate=int(self.info["defaultSampleRate"]), input=True)
            stream.close()
            return True
        except:
            return False

    def get_available_mics(self):
        """
        See which devices can be opened for microphone input.
        call this when no PyAudio object is loaded.
        """
        mics = []
        for device in range(self.audio_rec.get_device_count()):
            if self.valid_test(device):
                mics.append(device)
        if len(mics) == 0:
            raise N
        else:
            print("found %d microphone devices: %s" % (len(mics), mics))

        return mics

    ### SETUP AND SHUTDOWN

    def initialization(self):
        """run this after changing settings (like rate) before recording"""
        if self.device is None:
            self.device = self.get_available_mics()[0]  # pick the first one
        if self.rate is None:
            self.rate = self.valid_low_rate(self.device)
        self.chunk_size = int(self.rate / self.refresh_rate)  # hold one tenth of a second in memory
        if not self.valid_test(self.device, self.rate):
            print("guessing a valid microphone device/rate...")
            self.device = self.get_available_mics()[0]  # pick the first one
            self.rate = self.valid_low_rate(self.device)
        self.datax = np.arange(self.chunk_size) / float(self.rate)
        LOG.log_msg("Streaming from device: {0} with ID: {1} at rate: {2} Hz"
                    .format(self.info['name'], self.device, self.rate))

    def close(self):
        """gently detach from things."""
        print(" -- sending stream termination command...")
        self.keepRecording = False  # the threads should self-close
        while (self.t.isAlive()):  # wait for all threads to close
            time.sleep(.1)
        self.stream.stop_stream()
        self.audio_rec.terminate()

    ### STREAM HANDLING

    def stream_readchunk(self):
        """reads some audio and re-launches itself"""
        try:
            self.data = np.fromstring(self.stream.read(self.chunk_size), dtype=np.int16)
            self.fftx, self.fft = fourier_frequency(self.data, self.rate)

        except Exception as E:
            print(" -- exception! terminating...")
            print(E, "\n" * 5)
            self.keepRecording = False
        if self.keepRecording:
            self.stream_thread_new()
        else:
            self.stream.close()
            self.audio_rec.terminate()
            print(" -- stream STOPPED")
        self.chunksRead += 1

    def stream_thread_new(self):
        self.t = threading.Thread(target=self.stream_readchunk)
        self.t.start()

    def stream_start(self):
        """adds data to self.data until termination signal"""
        self.initialization()
        print(" -- starting stream")
        self.keepRecording = True  # set this to False later to terminate stream
        self.data = None  # will fill up with threaded recording data
        self.fft = None
        self.dataFiltered = None  # same
        self.stream = self.audio_rec.open(format=pyaudio.paInt16, channels=1,
                                          rate=self.rate, input=True, frames_per_buffer=self.chunk_size)
        self.stream_thread_new()
