"""Suppress some errors and send warning message."""

from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound, BotBlocked

from loader import dp
from texts import main as texts


@dp.message_handler(content_types='any', state='*', chat_type='private')
@dp.callback_query_handler(state='*', chat_type='private')
async def error():
    return texts.error


@dp.errors_handler(exception=MessageNotModified)
async def suppress_error1():
    return True


@dp.errors_handler(exception=MessageToDeleteNotFound)
async def suppress_error2():
    return True


@dp.errors_handler(exception=BotBlocked)
async def suppress_error3():
    return True
