class MicrophoneDeviceNotFound(Exception):
    """No microphones were found"""

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class DataStreamVisualizationError(Exception):
    """Error occurs while processing data from microphone"""

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
