"""Suppress some errors and send warning message."""

import logging
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound

from loader import dp
from questions.misc import HandleException

logger = logging.getLogger(__name__)
Update = Union[types.Message, types.CallbackQuery]


@dp.message_handler(content_types='any', state='*')
@dp.callback_query_handler(state='*')
async def error(update: Update, state: FSMContext):
    logger.info('ERROR ON: %s', [str(update), await state.get_state()])
    return HandleException('Ошибка, попробуйте еще раз или сделайте сброс через /cancel')


@dp.errors_handler(exception=MessageNotModified)
async def suppress_error1(*args):
    logger.info('ERROR ON: %s', args)
    return True


@dp.errors_handler(exception=MessageToDeleteNotFound)
async def suppress_error2(*args):
    logger.info('ERROR ON: %s', args)
    return True
