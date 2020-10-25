from threading import Thread

import numpy as np
from audiolazy.lazy_analysis import stft, window
from audiolazy.lazy_io import AudioIO

from monitor.mics import Microphone, open_microphone_stream


class AudioListener:
    def __init__(self, mic: Microphone, sample_rate: int = 20):
        self.data = None
        self.fft_data = None
        self.fft_frequency = None
        self.phase_shift = 0
        self.stream = open_microphone_stream(mic, sample_rate)

    def run(self):
        """
        Run audio listener - reading data from audio input device (microphone).
        Listening is performed in separate thread - non blocking.
        """
        listener_thread = Thread(target=self._read_data_chunk, args=())
        listener_thread.daemon = True
        listener_thread.start()

    def _read_data_chunk(self):
        """
        Read data from input device (microphone) and apply roll spectrum algorithm on it.
        Recorded audio is played back using AudioIO (from audiolazy library)
        with spectrum modification applied on it too.
        """
        chunk = self.stream.chunk_size

        @stft(size=chunk, hop=682, wnd=window.hann, ola_wnd=window.hann)
        def _roll_spectrum(data: np.ndarray) -> np.ndarray:
            if self.phase_shift != 0:
                abs_data = abs(data)
                phases = np.angle(data)
                return np.roll(abs_data, self.phase_shift) * np.exp(1j * phases)
            return data

        with AudioIO(True) as pr:
            pr.play(_roll_spectrum(pr.record()))
            while True:
                raw_data = self.stream.read()
                self.data = np.fromstring(raw_data, dtype=np.float32)
                self._recalculate_fourier_frequencies()

    def _recalculate_fourier_frequencies(self):
        """
        Recalculates data (fft_frequency, fft_data) used for the sound frequency visualization.
        Frequencies are calculated by applying fft onto raw data gathered from sound input device.
        Only half of the data is resigned to values for better visualization experience -
        first half of the data is usually mostly a 0 values.
        """
        fft = np.abs(np.fft.fft(self.data))
        freq = np.fft.fftfreq(len(fft), 1.0 / self.stream.microphone.sample_rate)

        self.fft_frequency = freq[:int(len(freq) / 2)]
        self.fft_data = fft[:int(len(fft) / 2)]
