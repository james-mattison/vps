from datetime import datetime


def unixtime_to_string(stamp: int,
                       fmt: str = "%a %d %b %Y, %I:%M%p") -> str:
    """
    UNIX timestamp to formatted time.
    """
    when = datetime.fromtimestamp(int(stamp))
    return when.strftime(fmt)

def datetime_to_unixtime(timestring: str,
                         format: str = "%a %d %b %Y, %I:%M%p") -> int:

    when = datetime.strptime(timestring, format)
    return int(when.strftime("+%s"))
