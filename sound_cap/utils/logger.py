import logging


class Singleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]


class Logger(metaclass=Singleton):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.StreamHandler()
        self.format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.format)
        self.logger.addHandler(self.handler)

    def log_msg(self, msg):
        self.logger.log(self.logger.getEffectiveLevel(),
                        msg)

    def error_msg(self, msg):
        self.logger.error(msg)

    def set_logging_lvl(self, level):
        log_level = logging.getLevelName(level)
        self.logger.setLevel(log_level)
