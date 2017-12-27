import logging


class Singleton(type):
    _instance = {}

    def __call__(self, cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]


class Logger(metaclass=Singleton):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.handler = logging.StreamHandler()
        self.format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setLevel(logging.INFO)
        self.handler.setFormatter(self.format)
        self.logger.addHandler(self.handler)

    def info_msg(self, msg):
        self.logger.info(msg)

    def set_logging_lvl(self, level):
        log_level = logging.getLevelName(level)
        self.logger.setLevel(log_level)
