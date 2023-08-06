from collections.abc import Awaitable, Callable
from typing import TypeVar

from asyncpraw.models.reddit.comment import Comment, CommentModeration
from asyncpraw.models.reddit.submission import Submission, SubmissionModeration

ContentType = Submission | Comment
ModType = SubmissionModeration | CommentModeration

T_Content = TypeVar("T_Content", Submission, Comment)
T_Mod = TypeVar("T_Mod", SubmissionModeration, CommentModeration)

Handler = Callable[[T_Content, T_Mod], Awaitable[None]]
