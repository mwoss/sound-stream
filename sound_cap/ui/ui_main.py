# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_AudioVisualizer(object):
    def setupUi(self, AudioVisualizer):
        AudioVisualizer.setObjectName(_fromUtf8("AudioVisualizer"))
        AudioVisualizer.resize(1000, 700)
        AudioVisualizer.setStyleSheet(_fromUtf8("background-color: #283747"))
        self.centralwidget = QtGui.QWidget(AudioVisualizer)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.sound_lvl = QtGui.QProgressBar(self.centralwidget)
        self.sound_lvl.setMaximum(1000)
        self.sound_lvl.setProperty("value", 150)
        self.sound_lvl.setTextVisible(False)
        self.sound_lvl.setOrientation(QtCore.Qt.Vertical)
        self.sound_lvl.setObjectName(_fromUtf8("sound_lvl"))
        self.horizontalLayout.addWidget(self.sound_lvl)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_fft = QtGui.QLabel(self.frame)
        self.label_fft.setStyleSheet(_fromUtf8("color: #FFFFFF"))
        self.label_fft.setObjectName(_fromUtf8("label_fft"))
        self.verticalLayout.addWidget(self.label_fft)
        self.fft_plot = PlotWidget(self.frame)
        self.fft_plot.setObjectName(_fromUtf8("fft_plot"))
        self.verticalLayout.addWidget(self.fft_plot)
        self.pcm_normal = QtGui.QLabel(self.frame)
        self.pcm_normal.setStyleSheet(_fromUtf8("color: #FFFFFF"))
        self.pcm_normal.setObjectName(_fromUtf8("pcm_normal"))
        self.verticalLayout.addWidget(self.pcm_normal)
        self.pcm_plot = PlotWidget(self.frame)
        self.pcm_plot.setObjectName(_fromUtf8("pcm_plot"))
        self.verticalLayout.addWidget(self.pcm_plot)
        self.horizontalLayout.addWidget(self.frame)
        AudioVisualizer.setCentralWidget(self.centralwidget)

        self.retranslateUi(AudioVisualizer)
        QtCore.QMetaObject.connectSlotsByName(AudioVisualizer)

    def retranslateUi(self, AudioVisualizer):
        AudioVisualizer.setWindowTitle(_translate("AudioVisualizer", "AudioVisualizer", None))
        self.label_fft.setText(_translate("AudioVisualizer", "Frequency data:", None))
        self.pcm_normal.setText(_translate("AudioVisualizer", "Pulse-code modulation:", None))


from pyqtgraph import PlotWidget
