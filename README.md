# Audio streaming with data visualization
Application allowing real-time sound streaming with visualization gathered data as frequency spectrum
plot and pulse code modulation plot. Program also allows to modulate voice in real-time using phase vocoder from audiolazy library.

Code can be used on Raspberry Pi, as well as on the desktops.

Shout out to Scott W Harden for sharing publication I based my project on: [SWHarden.com](https://www.swharden.com/wp/2016-07-31-real-time-audio-monitor-with-pyqt/)

## Usage
Running this application is dead simple, just execute below command :D
```shell script
python3 app.py
```

for compiling .ui XML files created via QT Creator run `convert_qt_ui` script 
located in folder `script/` directory
```shell script 
python3 convert_qt_ui.py ../resources/qt_ui.ui
```


## Application setup
On PC and Mac you can use install almost all dependencies using `pip`.

Instruction for installing necessary libraries on Raspberry Pi in libs_install_inst.pdf (Polish language).
 

