# Audio streaming with data visualization [WIP]
Application allowing real-time sound streaming with visualization gathered data as frequency spectrum
plot and pulse code modulation plot.

Code can be used on Raspberry Pi, as well as on normal PC.
## Usage
```angular2html
 >> python3 stream_s.py
```
for compiling .ui XML files created via QT Creator run qtUI_converter script 
located in folder sound_cap/utils
```angular2html
 python3 qtUI_converter.py [xml_file_directory]
 
 >> python3 qtUI_converter.py ../resources/qt_ui.ui
```


## Requirements
 - Python 3.X
 - Numpy 
 - Pyaudio 
 - PyQt4 
 - Pyqtgraph 

##### Note: Instruction for installing necessary libraries on Raspberry Pi in libs_install_inst.pdf (Polish language). On PC you can use pip for almost every libraries, expect for PyQt4 on Windows. You have to download pyqt4 wheel file from [lfd.uci.edu](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4) and execute it using pip install command.