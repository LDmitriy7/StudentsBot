from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

from loader import dp
from questions.misc import HandleException


@dp.message_handler(content_types='any', state='*')
@dp.callback_query_handler(state='*')
async def error(msg: types.Message):
    return HandleException('Ошибка, попробуйте еще раз или сделайте сброс через /cancel')


@dp.errors_handler(exception=MessageNotModified)
async def suppress_error(*args):
    return True
