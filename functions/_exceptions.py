from aiogram import types
from aiogram.contrib.middlewares.conversation import HandleException
from collections.abc import Awaitable, Callable

__all__ = ['process_exception']


async def process_exception(exception: HandleException):
    msg = types.Message.get_current()
    e_body = exception.on_exception

    if isinstance(e_body, str):
        await msg.answer(e_body)
    elif isinstance(e_body, Awaitable):
        await e_body
    elif isinstance(e_body, Callable):
        await e_body()
