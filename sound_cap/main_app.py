from sys import argv, exit
import numpy as np
import pyqtgraph
from PyQt4 import QtGui, QtCore

import sound_cap.SWHear as SWHear
import sound_cap.ui_main as ui_main
from sound_cap.utils.logger import Logger

LOG = Logger()


class SoundStream(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')  # before loading widget
        super(SoundStream, self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet("background-color: #283747;")
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        self.maxFFT = 0
        self.maxPCM = 0
        self.ear = SWHear.SWHear(refresh_rate=20)
        self.ear.stream_start()

    def update(self):
        if self.ear.data is not None and self.ear.fft is not None:
            pcmMax = np.max(np.abs(self.ear.data))
            if pcmMax > self.maxPCM:
                self.maxPCM = pcmMax
                self.grPCM.plotItem.setRange(yRange=[-pcmMax, pcmMax])
            if np.max(self.ear.fft) > self.maxFFT:
                self.maxFFT = np.max(np.abs(self.ear.fft))
                # self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
                self.grFFT.plotItem.setRange(yRange=[0, 1])
            self.pbLevel.setValue(1000 * pcmMax / self.maxPCM)
            pen = pyqtgraph.mkPen(color='b')
            self.grPCM.plot(self.ear.y_points, self.ear.data, pen=pen, clear=True)
            pen = pyqtgraph.mkPen(color='r')
            self.grFFT.plot(self.ear.fftx, self.ear.fft / self.maxFFT, pen=pen, clear=True)
        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat


def main():
    LOG.log_msg("Start sound streaming.")
    app = QtGui.QApplication(argv)
    window = SoundStream()
    window.show()
    window.update()
    exit(app.exec_())
    LOG.log_msg("Sound streaming closed")
