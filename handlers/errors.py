"""Suppress some errors and send warning message."""

from aiogram.contrib.middlewares.conversation import HandleException
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound, BotBlocked

from loader import dp
from texts import main as texts


@dp.message_handler(content_types='any', state='*', chat_type='private')
@dp.callback_query_handler(state='*', chat_type='private')
async def error(*args):
    return HandleException(texts.error)


@dp.errors_handler(exception=MessageNotModified)
async def suppress_error1(*args):
    return True


@dp.errors_handler(exception=MessageToDeleteNotFound)
async def suppress_error2(*args):
    return True


@dp.errors_handler(exception=BotBlocked)
async def suppress_error3(*args):
    return True
