# log_config.py
import logging
from datetime import datetime
import pytz

class ItalyTimeFormatter(logging.Formatter):
    def converter(self, timestamp):
        utc_time = datetime.utcfromtimestamp(timestamp)
        italy_time = utc_time.astimezone(pytz.timezone('Europe/Rome'))
        return italy_time.timetuple()

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Elimina todos los controladores existentes antes de agregar uno nuevo
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    log_format = ItalyTimeFormatter('%(asctime)s %(levelname)s - %(message)s')

    # Agrega un controlador de transmisión con el formato personalizado al registrador
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    logger.addHandler(stream_handler)

    return logger

logger = setup_logger()