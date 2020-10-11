import logging
from sys import argv

from PyQt5.QtWidgets import QApplication

from sound_cap.audio_exceptions import MicrophoneDeviceNotFound
from sound_cap.main_app import SoundStreamVisualization


def main():
    app = QApplication(argv)
    window = SoundStreamVisualization()

    try:
        window.show()
        window.update()
        app.exec_()
    except KeyError as e:
        logging.error(str(e) + " - User level error")
    except MicrophoneDeviceNotFound as e:
        logging.error(str(e) + " - Device level error")
    except (ValueError, TypeError) as e:
        window.audio.audio_rec.close()
        logging.error(str(e) + " - Application level error")
    finally:
        logging.info("Application is closed")
        del app


if __name__ == '__main__':
    main()
