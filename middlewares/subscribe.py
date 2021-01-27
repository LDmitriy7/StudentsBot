from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from config import MAIN_CHANNEL
from loader import bot
from aiogram.utils.exceptions import BadRequest


class CheckSubscription(BaseMiddleware):
    exception_text = f'Ошибка, сначала подпишитесь на канал {MAIN_CHANNEL}'

    @classmethod
    async def on_pre_process_message(cls, msg: types.Message, *args):
        if not await _is_chat_member(msg.from_user.id):
            await msg.answer(cls.exception_text)
            raise CancelHandler

    @classmethod
    async def on_pre_process_callback_query(cls, query: types.CallbackQuery, *args):
        if not await _is_chat_member(query.from_user.id):
            await query.message.answer(cls.exception_text)
            raise CancelHandler


async def _is_chat_member(user_id: int):
    try:
        chat_member = await bot.get_chat_member(MAIN_CHANNEL, user_id)
        if chat_member.is_chat_member():
            return True
    except BadRequest:
        pass

    return False
