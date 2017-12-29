import pyaudio
import time
import numpy as np
import threading

from sound_cap.utils.logger import Logger
from sound_cap.utils.audio_exceptions import MicrophoneDeviceNotFound

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

    def __init__(self, device=1, refresh_rate=10):
        self.audio_rec = pyaudio.PyAudio()
        self.devices_name = []
        self.mics_rate = []
        self.chunk_size = 4096
        self.chunksRead = 0
        self.refresh_rate = refresh_rate
        self.devices_id = self.get_available_mics()

    def valid_low_rate(self, device):
        """set the rate to the lowest supported audio rate."""
        for testrate in [44100]:
            if self.validation_test(device):
                return testrate
        print("SOMETHING'S WRONG! I can't figure out how to use DEV", device)
        return None

    def validation_test(self, device):
        LOG.log_msg("Checking device ID: {0}".format(device))
        info = self.audio_rec.get_device_info_by_index(device)
        if info["maxInputChannels"] <= 0:
            return False
        try:
            stream = self.audio_rec.open(format=pyaudio.paInt16, channels=1,
                                         input_device_index=device,
                                         frames_per_buffer=self.chunk_size,
                                         rate=int(info["defaultSampleRate"]),
                                         input=True)

            stream.close()
            LOG.log_msg("Device ID: {0} is working properly".format(device))
            self.devices_name.append(info['name'])
            self.mics_rate.append(int(info["defaultSampleRate"]))
            return True
        except ValueError:
            LOG.log_msg("Device ID: {0} isnt working".format(device))
            return False

    def get_available_mics(self):
        LOG.log_msg("Searching for microphones devices")
        mics = []
        for device in range(self.audio_rec.get_device_count()):
            if self.validation_test(device):
                mics.append(device)
        if len(mics) == 0:
            raise MicrophoneDeviceNotFound
        LOG.log_msg("Microphones found: {0}".format(mics))
        return mics

    def initialization(self):
        """run this after changing settings (like rate) before recording"""
        self.chunk_size = int(self.mics_rate[0] / self.refresh_rate)
        self.y_points = np.arange(self.chunk_size) / float(self.mics_rate[0])
        LOG.log_msg("Streaming from device: {0} with ID: {1} at rate: {2} Hz"
                    .format(self.devices_name[0], self.devices_id[0], self.mics_rate[0]))

    def close(self):
        """gently detach from things."""
        print(" -- sending stream termination command...")
        self.keepRecording = False  # the threads should self-close
        while (self.t.isAlive()):  # wait for all threads to close
            time.sleep(.1)
        self.stream.stop_stream()
        self.audio_rec.terminate()

    def stream_readchunk(self):
        """reads some audio and re-launches itself"""
        try:
            self.data = np.fromstring(self.stream.read(self.chunk_size), dtype=np.int16)
            self.fftx, self.fft = fourier_frequency(self.data, self.mics_rate[0])

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
                                          rate=self.mics_rate[0], input=True, frames_per_buffer=self.chunk_size)
        self.stream_thread_new()
