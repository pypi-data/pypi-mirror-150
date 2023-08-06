from comis import check
from comis.utils import ContentType


def karma_gt(
    total: int = None,
    *,
    post: int = None,
    comment: int = None,
    awardee: int = None,
    awarder: int = None,
    link: int = None
):
    """
    Filter posts by type of karma greater than the given value.

    Parameters
    ----------
    total :
        The total karma to check against.
    post :
        The post karma to check against.
    comment :
        The comment karma to check against.
    awardee :
        The awardee karma to check against.
    awarder :
        The awarder karma to check against.
    link :
        The link karma to check against.

    """

    async def predicate(content: ContentType, _):
        author = content.author
        await author.load()

        if total is not None:
            if author.total_karma > total:
                return False
        if post is not None:
            if author.post_karma > post:
                return False
        if comment is not None:
            if author.comment_karma > comment:
                return False
        if awardee is not None:
            if author.awardee_karma > awardee:
                return False
        if awarder is not None:
            if author.awarder_karma > awarder:
                return False
        if link is not None:
            if author.link_karma > link:
                return False
        return True

    return check(predicate)
