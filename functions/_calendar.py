"""Contain funcs for work with inline calendar."""
from datetime import date
from typing import Union

from aiogram import types
from aiogram.contrib.questions import QuestFunc

from keyboards import inline_funcs
from loader import calendar
from subfuncs.currents2 import Currents
from utils.inline_calendar import NotInitedException

__all__ = ['handle_calendar_callback']


@Currents.set
async def handle_calendar_callback(callback_data, *, query: types.CallbackQuery) -> Union[date, QuestFunc]:
    """Return date or exception for turning/reiniting calendar."""
    try:
        _date = calendar.handle_callback(query.from_user.id, callback_data)
    except NotInitedException:
        await query.answer('Попробуйте еще раз')
        return QuestFunc(_reinit_calendar)

    if _date is None:
        return QuestFunc(_turn_calendar)
    return _date


@Currents.set
async def _reinit_calendar(*, query_msg: types.Message):
    keyboard = inline_funcs.make_calendar()
    await query_msg.edit_reply_markup(keyboard)


@Currents.set
async def _turn_calendar(*, query_msg: types.Message):
    keyboard = calendar.get_keyboard()
    await query_msg.edit_reply_markup(keyboard)
