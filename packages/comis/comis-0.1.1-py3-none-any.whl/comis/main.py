from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from inspect import signature
from typing import Any, Literal

from asyncpraw import Reddit
from asyncpraw.models import Comment
from asyncpraw.models.reddit.comment import Comment, CommentModeration
from asyncpraw.models.reddit.submission import Submission, SubmissionModeration

from .utils import ContentType, Handler, ModType

_logger = logging.getLogger(__name__)

_valid_events = ("post", "comment")


class Event:
    events: dict[Literal["submission", "comment"], list[Event]] = {
        "submission": [],
        "comment": [],
    }

    def __init__(
        self,
        evt: str,
        evt_type: Literal["submission", "comment"],
        handler: Callable[[ContentType, ModType], Awaitable[None]],
        criteria: dict[str, Any],
    ):
        """

        Parameters
        ----------
        evt :
            Event name.
        evt_type :
            Event type.
        handler :
            Handler function.
        criteria :
            Criteria to match.
        """
        self.event: str = evt
        self.handler: Callable[[ContentType, ModType], Awaitable[None]] = handler
        self.criteria: dict[str, Any] = criteria

        self.events[evt_type].append(self)

        self.before: list[Callable[[ContentType, ModType], Awaitable[bool]]] = []

    async def __call__(self, *args, **kwargs):
        print(args, kwargs)
        for predicate in self.before:
            if not await predicate(*args, **kwargs):
                break
        else:
            await self.handler(self, *args, **kwargs)


def submission(
    **kwargs,
) -> Callable[[Callable[[Submission, SubmissionModeration], Awaitable[None]]], Event]:
    """
    Decorator for handling submission events.

    Examples
    --------

    .. code-block:: python

        @submission()
        async def handle_submission(self, submission, mod):
            comment = await submission.reply("Beep boop, this is an automated mod message.")
            await comment.mod.distinguish(how="yes", sticky=True)
    """

    def wrapper(handler: Callable[[Submission, SubmissionModeration], Awaitable[None]]):
        e = Event(handler.__name__, "submission", handler, kwargs)

        for condition in kwargs:
            pass

        return e

    return wrapper


def comment(**kwargs) -> Callable[[Handler[Comment, CommentModeration]], Event]:
    """
    Decorator for handling comment events.

    Examples
    --------

    .. code-block:: python

        @comment()
        async def handle_comment(self, comment, mod):
             if comment.author == (await self.reddit.user.me()):
                 await mod.approve()
                 await mod.distinguish(how="yes")
    """

    def wrapper(handler: Callable[[Comment, CommentModeration], Awaitable[None]]):
        return Event(handler.__name__, "comment", handler, kwargs)

    return wrapper


class Client:
    """
    A Client for interacting with Reddit.

    Parameters
    ----------
    client_id :
        The client ID for the application.
    client_secret :
        The client secret for the application.
    user_agent :
        The user agent for the application.
    username :
        The username for the account.
    password :
        The password for the account.
    subreddits:
        The subreddits to monitor.


    Examples
    --------

    .. code-block:: python

        from comis import Client

        bot = Client(
            client_id="Ur3l0nG3fA5a.dasfh41vcFQA453d",
            client_secret="uAfgk1fhdjlk...",
            user_agent="comis reddit bot by /u/endercheif",
            username="endercheif",
            password="supersecretpassword",
            subreddits=["your_subreddit"],
        )

        bot.run()
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
        subreddits: list[str],
    ):

        self._create_reddit = lambda: Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )

        self.reddit: Reddit = None  # type: ignore

        self.subreddits = subreddits
        self._subreddits = "+".join(subreddits)

    async def process(self, payload: ContentType) -> None:
        evt_type = "submission" if isinstance(payload, Submission) else "comment"
        for evt in Event.events[evt_type]:  # type: ignore
            sig = signature(evt.handler)
            if sig.parameters.get("self", None) is not None:
                await evt.handler(self, payload, payload.mod)  # type: ignore
            else:
                await evt.handler(payload, payload.mod)

    async def _run(self):
        print(self)
        if self.reddit is None:
            self.reddit = self._create_reddit()

        async for post in (
            await self.reddit.subreddit(self._subreddits)
        ).stream.submissions():
            await self.process(post)

    def run(self) -> None:
        asyncio.new_event_loop().run_until_complete(self._run())
