import logging
from sys import argv

from PyQt5.QtWidgets import QApplication

from monitor.mics import choose_microphone
from monitor.visualizer import SoundCaptureVisualizer

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)


def main():
    microphone = choose_microphone()

    app = QApplication(argv)
    visualizer = SoundCaptureVisualizer(microphone)

    try:
        visualizer.show()
        visualizer.update()
        app.exec_()
    except (ValueError, TypeError) as e:
        visualizer.close_sound_streaming()
        logging.error(e + " - Application level error")
    finally:
        logging.info("Application is closed")
        del app


if __name__ == "__main__":
    main()
