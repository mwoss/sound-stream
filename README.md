# Audio streaming with data visualization
Application allowing real-time sound streaming with visualization gathered data as frequency spectrum
plot and pulse code modulation plot. Program also allows to modulate voice in real-time using phase vocoder from audiolazy library.

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

