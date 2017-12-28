class MicrophoneDeviceNotFound(Exception):
    """No microphones were found"""
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
