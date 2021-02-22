"""Contain funcs for work with inline calendar."""
from datetime import date
from typing import Union

from aiogram import types
from aiogram.contrib.questions import QuestFunc

from keyboards import inline_funcs
from loader import calendar
from aiogram.contrib.currents import SetCurrent
from utils.inline_calendar import NotInitedException

__all__ = ['handle_calendar_callback']


@SetCurrent.query
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


@SetCurrent.query
async def _reinit_calendar(*, query: types.CallbackQuery):
    keyboard = inline_funcs.make_calendar()
    await query.message.edit_reply_markup(keyboard)


@SetCurrent.query
async def _turn_calendar(*, query: types.CallbackQuery):
    keyboard = calendar.get_keyboard()
    await query.message.edit_reply_markup(keyboard)
