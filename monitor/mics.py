import logging
from typing import Dict

import pyaudio

audio_rec = pyaudio.PyAudio()

HEALTH_CHECK_BUFFER_SIZE = 2048  # hard-coded buffer size for validation check


class MicrophoneDeviceNotFound(Exception):
    """No microphones were found"""


class Microphone:
    """
    Data class (compatibility with older Python version) that stores all basic information about microphone.
    """

    def __init__(self, mic_id: int, mic_name: str, sample_rate: int, input_channels: int):
        self.mic_id = mic_id
        self.mic_name = mic_name
        self.sample_rate = sample_rate
        self.input_channels = input_channels

    def __str__(self) -> str:
        return "Microphone ID: {}, Microphone name: {}, Sample rate: {}Hz, Input channels".format(
            self.mic_id, self.mic_name, self.sample_rate, self.input_channels
        )


class MicrophoneStream:
    """
    Convenient wrapper around pyaudio.Stream.
    Used for easy and painless use of pyaudio.Stream.read method with Microphone object.
    """

    def __init__(self, stream: pyaudio.Stream, microphone: Microphone, sample_rate: int):
        self.stream = stream
        self.microphone = microphone
        self.chunk_size = int(microphone.sample_rate / sample_rate)

    def read(self) -> str:
        return self.stream.read(self.chunk_size)

    def close(self):
        self.stream.close()


def open_microphone_stream(microphone: Microphone, sample_rate: int = 20) -> MicrophoneStream:
    """
    Opens PyAudio data stream using given microphone.
    :param microphone: Microphone used for data streaming
    :param sample_rate: Sampling rate of the input device
    :return: MicrophoneStream object - a convenient wrapper around PyAudio stream class
    """
    stream = audio_rec.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=microphone.sample_rate,
        input=True,
        frames_per_buffer=int(microphone.sample_rate / sample_rate),
    )
    return MicrophoneStream(stream, microphone, sample_rate)


def choose_microphone() -> Microphone:
    """
    Prompt a user input and ask user to choose microphone by entering device ID.
    :return: Chosen microphone as Microphone data class
    """
    logging.debug("Searching for microphones devices")
    devices_info = get_available_microphones()

    mic_id = int(input("Chose device by ID: "))  # retrieve device id from user

    if mic_id not in devices_info.keys():
        raise KeyError("Incorrect device ID")

    chosen_mic = devices_info[mic_id]
    logging.info(
        "Streaming from device: {} with ID: {} at rate: {} Hz".format(
            chosen_mic.mic_name, chosen_mic.mic_id, chosen_mic.sample_rate
        )
    )
    return chosen_mic


def get_available_microphones() -> Dict[int, Microphone]:
    """
    Search for all available microphones on given system an return dictionary with all of them.
    :return: dictionary where key is device ID and value is a Microphone data class
    """
    mics_info = {}

    for device_id in range(audio_rec.get_device_count()):
        device_info = audio_rec.get_device_info_by_index(device_id)
        microphone = Microphone(
            mic_id=device_id,
            mic_name=device_info["name"],
            sample_rate=int(device_info["defaultSampleRate"]),
            input_channels=device_info["maxInputChannels"],
        )

        if is_microphone_available(microphone):
            mics_info[device_id] = microphone

    if len(mics_info) == 0:
        raise MicrophoneDeviceNotFound("No mics found")

    logging.debug("{} available microphones were found".format(len(mics_info)))
    for mic_properties in mics_info.values():
        logging.info("Available microphone - specification - {}".format(mic_properties))

    return mics_info


def is_microphone_available(microphone: Microphone) -> bool:
    """
    Validates if given microphone can be used for data streaming.
    Validation is done by opening testing record stream and reading HEALTH_CHECK_BUFFER_SIZE of data.
    If reading succeed given microphone is marked as working and ready to use by application.
    :param microphone: microphone to validate
    :return: True if microphone is working properly and data stream can be opened, otherwise False
    """
    logging.debug("Checking availability of recoding device with ID: {}".format(microphone.mic_id))

    if microphone.input_channels <= 0:
        logging.error("Device ID: {} has no input channel. It's not usable for recording.".format(microphone.mic_id))
        return False

    try:
        stream = audio_rec.open(
            format=pyaudio.paInt16,
            channels=1,
            input_device_index=microphone.mic_id,
            frames_per_buffer=HEALTH_CHECK_BUFFER_SIZE,
            rate=microphone.sample_rate,
            input=True,
        )
        stream.close()
        logging.debug("Device ID: {} is working properly".format(microphone.mic_id))
    except (ValueError, OSError):
        logging.error("Device ID: {} is not working properly".format(microphone.mic_id))
        return False

    return True
