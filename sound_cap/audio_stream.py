import pyaudio
import time
import numpy as np
from threading import Thread
from audiolazy.lazy_analysis import stft, window
from audiolazy.lazy_io import AudioIO

from sound_cap.audio_exceptions import MicrophoneDeviceNotFound

import logging


def fourier_frequency(data, rate):
    fft = np.abs(np.fft.fft(data))
    freq = np.fft.fftfreq(len(fft), 1.0 / rate)
    return freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)]


class AudioStream:
    def __init__(self, refresh_rate=10):
        self.audio_rec = pyaudio.PyAudio()
        self.points_range = None
        self.data = None
        self.fft_data = None
        self.fft_frequency = None
        self.shift = 0
        self.__chunk_size = 2048
        self.__refresh_rate = refresh_rate
        self.__devices_info = {}
        self.__mic_id = None
        self.__stream = None

    def validation_test(self, device_id, mics_info):
        logging.info("Checking device ID: {0}".format(device_id))
        info = self.audio_rec.get_device_info_by_index(device_id)
        if info["maxInputChannels"] <= 0:
            logging.error("Max input channels <= 0")
            return
        try:
            stream = self.audio_rec.open(
                format=pyaudio.paInt16, channels=1,
                input_device_index=device_id,
                frames_per_buffer=self.__chunk_size,
                rate=int(info["defaultSampleRate"]),
                input=True
            )

            stream.close()
            logging.info("Device ID: {0} is working properly".format(device_id))
            mics_info[device_id] = {'mic_name': info['name'],
                                    'mic_rate': int(info["defaultSampleRate"])}
        except ValueError:
            logging.error("Device ID: {0} isnt working".format(device_id))

    def get_available_mics(self):
        logging.info("Searching for microphones devices")
        mics_info = {}
        for device in range(self.audio_rec.get_device_count()):
            self.validation_test(device, mics_info)
        if len(mics_info) == 0:
            raise MicrophoneDeviceNotFound("No mics found")
        logging.info("Microphones found: {0}".format(mics_info))
        return mics_info

    def choose_mic(self):
        logging.info("Choosing microphone")
        time.sleep(0.2)
        if len(self.__devices_info) >= 1:
            for mic_k, mic_val in self.__devices_info.items():
                print("Mic ID: {0}, specs: {1}".format(mic_k, mic_val))
            return int(input("Chose device by ID: "))
        return 0

    def initialization(self):
        logging.info("Initializing")
        self.__devices_info = self.get_available_mics()
        self.__mic_id = self.choose_mic()

        if self.__mic_id not in self.__devices_info.keys():
            raise KeyError("Incorrect device ID")

        self.__chunk_size = int(self.__devices_info[self.__mic_id]['mic_rate'] / self.__refresh_rate)
        self.points_range = np.arange(self.__chunk_size) / float(self.__devices_info[self.__mic_id]['mic_rate'])
        logging.info("Streaming from device: {0} with ID: {1} at rate: {2} Hz"
                     .format(self.__devices_info[self.__mic_id]['mic_name'],
                             self.__mic_id,
                             self.__devices_info[self.__mic_id]['mic_rate']))

    def read_data_chunk(self):
        chunk = self.__chunk_size

        @stft(size=chunk, hop=682, wnd=window.hann, ola_wnd=window.hann)
        def _roll_spectrum(data):
            if self.shift != 0:
                abs_data = abs(data)
                phases = np.angle(data)
                return np.roll(abs_data, self.shift) * np.exp(1j * phases)
            return data

        with AudioIO(True) as pr:
            pr.play(_roll_spectrum(pr.record()))
            while True:
                try:
                    raw_data = self.__stream.read(self.__chunk_size)
                    self.data = np.fromstring(raw_data, dtype=np.float32)
                    self.fft_frequency, self.fft_data = \
                        fourier_frequency(self.data, self.__devices_info[self.__mic_id]['mic_rate'])
                except (ValueError, TypeError):
                    raise

    def stream_start(self):
        self.initialization()
        self.__stream = self.audio_rec.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.__devices_info[self.__mic_id]['mic_rate'],
            input=True,
            frames_per_buffer=self.__chunk_size
        )

        main_thread = Thread(target=self.read_data_chunk, args=())
        main_thread.daemon = True
        main_thread.start()
