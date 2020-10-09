from sys import argv

from PyQt5.QtWidgets import QApplication

from sound_cap.main_app import SoundStreamVisualization


def main():
    # LOG.log_msg("Start sound streaming.")
    app = QApplication(argv)
    window = SoundStreamVisualization()

    try:
        window.show()
        window.update()
        app.exec_()
    # except KeyError as e:
    #     LOG.error_msg(str(e) + " - User level error")
    # except MicrophoneDeviceNotFound as e:
    #     LOG.error_msg(str(e) + " - Device level error")
    # except (ValueError, TypeError) as e:
    #     window.audio.audio_rec.close()
    #     LOG.error_msg(str(e) + " - Application level error")
    finally:
        print("Application is closed")
        del app


if __name__ == '__main__':
    main()
