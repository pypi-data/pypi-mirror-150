from datetime import datetime
from enum import IntEnum

from .. import check
from ..utils import ContentType


class Day(IntEnum):
    """Enum for days of the week."""

    monday = 1  #:
    tuesday = 2  #:
    wednesday = 3  #:
    thursday = 4  #:
    friday = 5  #:
    saturday = 6  #:
    sunday = 7  #:


def time(days: list[Day] = None):
    """
    Filter by time posted.

    Parameters
    ----------
    days :
        Valid days of the week.
    """

    async def wrapper(content: ContentType, __):
        d = datetime.utcfromtimestamp(content.created_utc).isoweekday()
        if days is not None:
            if d not in days:
                return False
        return True

    return check(wrapper)
