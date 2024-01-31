from datetime import datetime


def unixtime_to_string(timestring, fmt = "%a %d %b %Y, %I:%M%p"):
    when = datetime.fromtimestamp(int(timestring))
    return when.strftime(fmt)


def datetime_to_unixtime(time, format):
    return datetime.strftime(time, format)


