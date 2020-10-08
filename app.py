from sound_cap.main_app import main


def main():
    LOG.log_msg("Start sound streaming.")
    app = QtGui.QApplication(argv)
    window = SoundStreamVisualization()

    try:
        window.show()
        window.update()
        app.exec_()
    except KeyError as e:
        LOG.error_msg(str(e) + " - User level error")
    except MicrophoneDeviceNotFound as e:
        LOG.error_msg(str(e) + " - Device level error")
    except (ValueError, TypeError) as e:
        window.audio.audio_rec.close()
        LOG.error_msg(str(e) + " - Application level error")
    finally:
        LOG.log_msg("Application is closed")
        del app


if __name__ == '__main__':
    main()
