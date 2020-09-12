from datetime import datetime
import logging

from django.db import connection

from catalog.loggers.query_logger import QueryLogger
from catalog.loggers.query_logger_config import init_log
from catalog.utils import consts

main_log_name = consts.logs['main']
init_log(main_log_name)


def date_format_str(value, date_format=None):
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S.%f+00:00"
    to_datetime = datetime.strptime(value, date_format)
    to_str = '{0:02}.{1:02}.{2} {3:02}:{4:02}:{5:02}'.format(
        to_datetime.day, to_datetime.month, to_datetime.year,
        to_datetime.hour, to_datetime.minute, to_datetime.second)

    return to_str


def query_log(log_name=main_log_name):
    def on_call(func):
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(log_name)
            ql = QueryLogger()
            with connection.execute_wrapper(ql):
                result = func(*args, **kwargs)
            logger.info(str(ql))
            return result
        return wrapper
    return on_call
