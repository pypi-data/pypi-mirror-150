import pytz
import logging
import datetime


class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""
    def converter(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)
        tzinfo = pytz.timezone('Asia/Calcutta')
        return tzinfo.localize(dt)
        
    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s

def lvl_to_string(lvl):
    if lvl == 0:
        return 'NOTSET'
    elif lvl == 10:
        return 'DEBUG'
    elif lvl == 20:
        return 'INFO'
    elif lvl == 30:
        return 'WARNING'
    elif lvl == 40:
        return 'ERROR'
    elif lvl == 50:
        return 'CRITICAL'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def augment_http_message(method):
    def inner(ref, message, code, time=None):
        if time == None:
            augmented_message = f"{code} None \"{message}\""
        else:
            augmented_message = f"{code} {time:.2f}s \"{message}\""
        return method(ref, augmented_message, code, time)

    return inner

class HTTPLogger:

    def __init__(self, logger):

        datefmt = "%a %b %d %H:%M:%S %Y"
        http_format = '%(levelname)s: [%(asctime)s] HTTP/1.1 - %(object_id)s \'%(verb)s %(route)s\' %(message)s'

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            logging.Formatter(http_format, datefmt)
        )

        logger.addHandler(stream_handler)

        self.logger = logger

        self._object_id = None
        self._verb = None
        self._route = None

    @property
    def extra(self):
        return {
            'object_id': self._object_id,
            'verb': self._verb,
            'route': self._route
        }

    @property
    def object_id(self):
        return self._object_id

    @property
    def verb(self, verb):
        return self._verb

    @property
    def route(self, route):
        return self._route

    @object_id.setter
    def object_id(self, oid):
        self._object_id = oid

    @verb.setter
    def verb(self, verb):
        self._verb = verb

    @route.setter
    def route(self, route):
        self._route = route

    @augment_http_message
    def info(self, message, code, time=None):
        self.logger.info(message, extra=self.extra)

    @augment_http_message
    def debug(self, message, code, time=None):
        self.logger.debug(message, extra=self.extra)

    @augment_http_message
    def warning(self, message, code, time=None):
        self.logger.warning(message, extra=self.extra)

    @augment_http_message
    def error(self, message, code, time=None):
        self.logger.error(message, extra=self.extra)

    @property
    def level(self):
        return lvl_to_string(self.logger.level)

hlogger = HTTPLogger(logger)
