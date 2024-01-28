from datetime import datetime


def unixtime_to_string(timestring, fmt = "%m-%d-%y"):
    timestring = int(timestring)
    ret = datetime.strptime(timestring, fmt)
    return ret


def datetime_to_unixtime(time, format):
    return datetime.strftime(time, format)


