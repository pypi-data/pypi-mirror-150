from collections.abc import Awaitable
from typing import Any, Callable

from comis.utils import ContentType


def check(predicate: Callable[[ContentType, Any], Awaitable[bool]]):
    def decorator(func):
        func.before.append(predicate)
        return func

    return decorator
