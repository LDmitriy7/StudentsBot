"""Contain funcs for work with inline calendar."""
from datetime import date
from typing import Union

from aiogram import types

from keyboards import inline_funcs
from loader import calendar
from questions.misc import HandleException
from utils.inline_calendar import NotInitedException

__all__ = ['handle_calendar_callback']


async def handle_calendar_callback(query: types.CallbackQuery, callback_data) -> Union[date, HandleException]:
    """Return date or exception for turning/reiniting calendar."""
    try:
        _date = calendar.handle_callback(query.from_user.id, callback_data)
    except NotInitedException:
        await query.answer('Попробуйте еще раз')
        return HandleException(_reinit_calendar)

    if _date is None:
        return HandleException(_turn_calendar)
    return _date


async def _reinit_calendar(msg: types.Message):
    keyboard = inline_funcs.make_calendar()
    await msg.edit_reply_markup(keyboard)


async def _turn_calendar(msg: types.Message):
    keyboard = calendar.get_keyboard()
    await msg.edit_reply_markup(keyboard)
