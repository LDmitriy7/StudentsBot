from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

import functions as funcs
from config import CHANNEL_USERNAME


class CheckSubscription(BaseMiddleware):
    exception_text = f'Ошибка, сначала подпишитесь на канал {CHANNEL_USERNAME}'

    @classmethod
    async def on_pre_process_message(cls, msg: types.Message, *args):
        if not await funcs.is_channel_member():
            await msg.answer(cls.exception_text)
            raise CancelHandler

    @classmethod
    async def on_pre_process_callback_query(cls, query: types.CallbackQuery, *args):
        if not await funcs.is_channel_member():
            await query.message.answer(cls.exception_text)
            raise CancelHandler
