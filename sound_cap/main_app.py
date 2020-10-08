from sys import argv

import numpy as np
import pyqtgraph
from PyQt4 import QtGui, QtCore

import sound_cap.qt_ui as ui_main
from sound_cap.audio_stream import AudioStream
from sound_cap.audio_exceptions import MicrophoneDeviceNotFound


class SoundStreamVisualization(QtGui.QMainWindow, ui_main.Ui_AudioVisualizer):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')
        super(SoundStreamVisualization, self).__init__(parent)
        self.setupUi(self)
        self.fft_plot.plotItem.showGrid(True, True, 0.7)
        self.pcm_plot.plotItem.showGrid(True, True, 0.7)
        self.max_fft = 0
        self.max_normal = 0
        self.audio = AudioStream(refresh_rate=20)
        self.audio.stream_start()

    def update(self):
        if self.audio.data is not None and self.audio.fft_data is not None:
            temp_max = np.max(np.abs(self.audio.data))
            if temp_max > self.max_normal:
                self.max_normal = temp_max
                self.pcm_plot.plotItem.setRange(yRange=[-temp_max, temp_max])
            temp_fft_max = np.max(self.audio.fft_data)
            if temp_fft_max > self.max_fft:
                self.max_fft = temp_fft_max
                self.fft_plot.plotItem.setRange(yRange=[0, 1])
            self.sound_lvl.setValue(1000 * temp_max / self.max_normal)
            plot = pyqtgraph.mkPen(color='b')
            self.pcm_plot.plot(self.audio.points_range, self.audio.data, pen=plot, clear=True)
            plot = pyqtgraph.mkPen(color='r')
            self.fft_plot.plot(self.audio.fft_frequency, self.audio.fft_data / self.max_fft, pen=plot, clear=True)
            self.audio.shift = self.horizontalSlider.value()
        QtCore.QTimer.singleShot(1, self.update)



