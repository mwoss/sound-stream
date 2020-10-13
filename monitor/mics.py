import logging
from typing import Dict

import pyaudio

audio_rec = pyaudio.PyAudio()

HEALTH_CHECK_BUFFER_SIZE = 2048  # hard-coded buffer size for validation check


class MicrophoneDeviceNotFound(Exception):
    """No microphones were found"""


class Microphone:
    def __init__(self, mic_id: int, mic_name: str, sample_rate: int, input_channels: int):
        self.mic_id = mic_id
        self.mic_name = mic_name
        self.sample_rate = sample_rate
        self.input_channels = input_channels

    def __str__(self) -> str:
        return "Microphone ID: {}, Microphone name: {}, Sample rate: {}Hz, Input channels".format(
            self.mic_id,
            self.mic_name,
            self.sample_rate,
            self.input_channels
        )


class MicrophoneStream:

    def __init__(self, stream: pyaudio.Stream, microphone: Microphone, refresh_rate: int):
        self.stream = stream
        self.microphone = microphone
        self.chunk_size = int(microphone.sample_rate / refresh_rate)

    def read(self) -> str:
        return self.stream.read(self.chunk_size)

    def close(self):
        self.stream.close()


def open_microphone_stream(microphone: Microphone, refresh_rate: int = 20) -> MicrophoneStream:
    stream = audio_rec.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=microphone.sample_rate,
        input=True,
        frames_per_buffer=int(microphone.sample_rate / refresh_rate)
    )
    return MicrophoneStream(stream, microphone, refresh_rate)


def choose_microphone() -> Microphone:
    logging.debug("Searching for microphones devices")
    devices_info = get_available_microphones()

    mic_id = int(input("Chose device by ID: "))  # retrieve device id from user

    if mic_id not in devices_info.keys():
        raise KeyError("Incorrect device ID")

    chosen_mic = devices_info[mic_id]
    logging.info("Streaming from device: {} with ID: {} at rate: {} Hz".format(
        chosen_mic.mic_name,
        chosen_mic.mic_id,
        chosen_mic.sample_rate
    ))
    return chosen_mic


def get_available_microphones() -> Dict[int, Microphone]:
    mics_info = {}

    for device_id in range(audio_rec.get_device_count()):
        device_info = audio_rec.get_device_info_by_index(device_id)
        microphone = Microphone(
            mic_id=device_id,
            mic_name=device_info['name'],
            sample_rate=int(device_info["defaultSampleRate"]),
            input_channels=device_info["maxInputChannels"]
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
            input=True
        )
        stream.close()
        logging.debug("Device ID: {} is working properly".format(microphone.mic_id))
    except (ValueError, OSError):
        logging.error("Device ID: {} is not working properly".format(microphone.mic_id))
        return False

    return True
