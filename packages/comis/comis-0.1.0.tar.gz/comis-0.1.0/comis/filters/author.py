from datetime import datetime

from comis import check
from comis.utils import ContentType


def author(
    name: str = None,
    id: str = None,
    verified_email: bool = None,
    admin: bool = None,
    friend: bool = None,
    mod: bool = None,
    blocked: bool = None,
    premium: bool = None,
    suspended: bool = None,
    age: datetime = None,
):
    """
    Filter posts by author attributes.

    Examples
    --------

    .. code-block:: python

        from comis import Client, submission
        from comis.filters import author

        class MyClient(Client):
            @author(mod=False, premium=False)
            @submission()
            async def stuff(self, content, mod):
                await mod.remove()

    Parameters
    ----------
    name :
        Username of the author.
    id :
        ID of the author.
    verified_email :
        Whether the author has a verified email.
    admin :
        Whether the author is a site admin.
    friend :
        Whether the author is a friend.
    mod :
        Whether the author is a moderator of the subreddit.
    blocked :
        Whether the author is blocked by yourself.
    premium :
        Whether the author has reddit premium.
    suspended :
        Whether the author is a suspended account.
    age :
        Minimum of the author.

    """

    async def predicate(content: ContentType, _):
        a = content.author

        if name is not None and a.name != name:
            return False
        if id is not None and a.id != id:
            return False
        if verified_email is not None and a.has_verified_email is not verified_email:
            return False
        if admin is not None and a.is_employee is not admin:
            return False
        if friend is not None and a.is_friend is not friend:
            return False
        try:
            if mod is not None and a.is_mod is not mod:
                return False
        except AttributeError:
            pass
        if blocked is not None and a.is_blocked is not blocked:
            return False
        if premium is not None and a.is_gold is not premium:
            return False
        if suspended is not None and a.is_suspended is not suspended:
            return False
        if age is not None and float(a.age) != age.timestamp():
            return False
        return True

    return check(predicate)
