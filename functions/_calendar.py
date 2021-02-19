"""Contain funcs for work with inline calendar."""
from datetime import date
from typing import Union

from aiogram import types
from aiogram.contrib.questions import QuestFunc

from keyboards import inline_funcs
from loader import calendar
from subfuncs import decorators as current
from utils.inline_calendar import NotInitedException

__all__ = ['handle_calendar_callback']


@current.set_query
async def handle_calendar_callback(callback_data, query: types.CallbackQuery = None) -> Union[date, QuestFunc]:
    """Return date or exception for turning/reiniting calendar."""
    try:
        _date = calendar.handle_callback(query.from_user.id, callback_data)
    except NotInitedException:
        await query.answer('Попробуйте еще раз')
        return QuestFunc(_reinit_calendar)

    if _date is None:
        return QuestFunc(_turn_calendar)
    return _date


@current.set_query
async def _reinit_calendar(query: types.CallbackQuery = None):
    keyboard = inline_funcs.make_calendar()
    await query.message.edit_reply_markup(keyboard)


@current.set_query
async def _turn_calendar(query: types.CallbackQuery = None):
    keyboard = calendar.get_keyboard()
    await query.message.edit_reply_markup(keyboard)
