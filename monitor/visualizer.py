import numpy as np
import pyqtgraph
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow

from monitor.mics import Microphone
from monitor.listener import AudioListener
from monitor.qt_ui import Ui_AudioVisualizer


class SoundCaptureVisualizer(QMainWindow, Ui_AudioVisualizer):
    def __init__(self, input_device: Microphone, parent=None):
        pyqtgraph.setConfigOption('background', 'w')
        super(SoundCaptureVisualizer, self).__init__(parent)
        self.setupUi(self)
        self.fft_plot.plotItem.showGrid(True, True, 0.7)
        self.pcm_plot.plotItem.showGrid(True, True, 0.7)
        self.max_fft = 0
        self.max_normal = 0

        self._points_range = np.arange(int(input_device.sample_rate / 20)) / float(input_device.sample_rate)

        self._audio = AudioListener(input_device, sample_rate=20)
        self._audio.run()

    def update(self):
        if self._audio.data is not None and self._audio.fft_data is not None:
            temp_max = np.max(np.abs(self._audio.data))

            if temp_max > self.max_normal:
                self.max_normal = temp_max
                self.pcm_plot.plotItem.setRange(yRange=[-temp_max, temp_max])

            temp_fft_max = np.max(self._audio.fft_data)

            if temp_fft_max > self.max_fft:
                self.max_fft = temp_fft_max
                self.fft_plot.plotItem.setRange(yRange=[0, 1])

            self.sound_lvl.setValue(1000 * temp_max / self.max_normal)
            plot = pyqtgraph.mkPen(color='b')
            self.pcm_plot.plot(self._points_range, self._audio.data, pen=plot, clear=True)
            plot = pyqtgraph.mkPen(color='r')
            self.fft_plot.plot(self._audio.fft_frequency, self._audio.fft_data / self.max_fft, pen=plot, clear=True)
            self._audio.phase_shift = self.horizontalSlider.value()

        QtCore.QTimer.singleShot(1, self.update)

    def close_sound_streaming(self):
        self._audio.stream.close()
