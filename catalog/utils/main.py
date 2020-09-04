from datetime import datetime


def date_format_str(value, date_format=None):
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S.%f+00:00"
    to_datetime = datetime.strptime(value, date_format)
    to_str = '{0:02}.{1:02}.{2} {3:02}:{4:02}:{5:02}'.format(
        to_datetime.day, to_datetime.month, to_datetime.year,
        to_datetime.hour, to_datetime.minute, to_datetime.second)

    return to_str
