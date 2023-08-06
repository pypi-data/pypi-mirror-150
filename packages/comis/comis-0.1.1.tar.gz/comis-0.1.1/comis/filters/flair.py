from __future__ import annotations

from re import Pattern
from typing import Optional

from comis import check


def flair(
    text: Optional[str | Pattern] = None,
    flaired: bool = None,
    template_id: str = None,
    color: str = None,
    colour: str = None,
    type: str = None,
):
    """
    Filter by flair properties.

    Parameters
    ----------
    text :
        Text or Regular Expression to match against flair text.
    flaired :
        Whether the post is flaired.
    template_id :
        Template ID for flair.
    color :
        Color for flair.
    colour :
        Colour for flair.
    type :
        Type for flair.

    Returns
    -------

    """

    async def predicate(post, mod):
        if text is not None:
            if isinstance(text, Pattern):
                if not text.search(post.title):
                    return False
            elif text != post.title:
                return False

        if flaired is not None:
            if flaired and post.link_flair_text is None:
                return False
            elif not flaired and post.link_flair_text is not None:
                return False

        if template_id is not None:
            if post.link_flair_template_id != template_id:
                return False

        if color is not None:
            if post.link_flair_text_color != color:
                return False

        if colour is not None:
            if post.link_flair_text_color != colour:
                return False

        if type is not None:
            if post.link_flair_type != type:
                return False

        return True

    return check(predicate)
