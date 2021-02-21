import functools
from typing import Awaitable, Callable

from aiogram import types, Dispatcher

AsyncFunction = Callable[..., Awaitable]


def set_user(func) -> AsyncFunction:
    """Set user = current User [if user not provided]."""

    @functools.wraps(func)
    async def wrapper(*args, user: types.User = None, **kwargs):
        if user is None:
            user = types.User.get_current()
        return await func(*args, **kwargs, user=user)

    return wrapper


def set_chat(func) -> AsyncFunction:
    """Set chat = current Chat [if chat not provided]."""

    @functools.wraps(func)
    async def wrapper(*args, chat: types.Chat = None, **kwargs):
        if chat is None:
            chat = types.Chat.get_current()
        return await func(*args, **kwargs, chat=chat)

    return wrapper


def set_query(func) -> AsyncFunction:
    """Set query = current CallbackQuery [if query not provided]."""

    @functools.wraps(func)
    async def wrapper(*args, query: types.CallbackQuery = None, **kwargs):
        if query is None:
            query = types.CallbackQuery.get_current()
        return await func(*args, **kwargs, query=query)

    return wrapper


def set_inline_query(func) -> AsyncFunction:
    """Set query = current InlineQuery [if query not provided]."""

    @functools.wraps(func)
    async def wrapper(*args, query: types.InlineQuery = None, **kwargs):
        if query is None:
            query = types.InlineQuery.get_current()
        return await func(*args, **kwargs, query=query)

    return wrapper


def set_msg(func) -> AsyncFunction:
    """Set msg = current Message [if msg is not provided]."""

    @functools.wraps(func)
    async def wrapper(*args, msg: types.Message = None, **kwargs):
        if msg is None:
            msg = types.Message.get_current()
        return await func(*args, **kwargs, msg=msg)

    return wrapper


def set_udata(func) -> AsyncFunction:
    """Set udata = storage data for current User+Chat [if udata is not provided]."""

    @functools.wraps(func)
    async def wrapper(*args, udata: dict = None, **kwargs):
        if udata is None:
            udata = await Dispatcher.get_current().current_state().get_data()
        return await func(*args, **kwargs, udata=udata)

    return wrapper
