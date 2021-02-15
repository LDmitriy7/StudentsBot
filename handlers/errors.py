"""Suppress some errors and send warning message."""

import logging
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound, BotBlocked

from loader import dp
from datatypes import HandleException
from texts import main as texts

logger = logging.getLogger(__name__)
Update = Union[types.Message, types.CallbackQuery]


@dp.message_handler(content_types='any', state='*', chat_type='private')
@dp.callback_query_handler(state='*', chat_type='private')
async def error(update: Update, state: FSMContext):
    logger.info('ERROR ON: %s', [str(update), await state.get_state()])
    return HandleException(texts.error)


@dp.errors_handler(exception=MessageNotModified)
async def suppress_error1(*args):
    logger.info('ERROR ON: %s', [str(i) for i in args])
    return True


@dp.errors_handler(exception=MessageToDeleteNotFound)
async def suppress_error2(*args):
    logger.info('ERROR ON: %s', [str(i) for i in args])
    return True


@dp.errors_handler(exception=BotBlocked)
async def suppress_error3(*args):
    logger.info('ERROR ON: %s', [str(i) for i in args])
    return True
