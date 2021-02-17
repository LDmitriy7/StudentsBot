import functools
from typing import Awaitable, Callable
from aiogram import types

AsyncFunction = Callable[..., Awaitable]


def set_user(func) -> AsyncFunction:
    """Set user = current User [if user not provided]."""

    @functools.wraps(func)
    async def wrapper(*args, user: types.User = None, **kwargs):
        if user is None:
            user = types.User.get_current()
        return await func(*args, user=user, **kwargs)

    return wrapper


def set_chat(func) -> AsyncFunction:
    """Set chat = current Chat [if chat not provided]."""

    @functools.wraps(func)
    async def wrapper(*args, chat: types.Chat = None, **kwargs):
        if chat is None:
            chat = types.Chat.get_current()
        return await func(*args, chat=chat, **kwargs)

    return wrapper


def set_query(func) -> AsyncFunction:
    """Set query = current Query [if query not provided]."""

    @functools.wraps(func)
    async def wrapper(*args, query: types.CallbackQuery = None, **kwargs):
        if query is None:
            query = types.CallbackQuery.get_current()
        return await func(*args, query=query, **kwargs)

    return wrapper
