"""Contain funcs for work with inline calendar."""
from datetime import date
from typing import Union

from aiogram import types
from aiogram.contrib.questions import QuestFunc
from aiogram.dispatcher.currents import CurrentObjects

from keyboards import inline_funcs
from loader import calendar
from utils.inline_calendar import NotInitedException

__all__ = ['handle_calendar_callback']


@CurrentObjects.decorate
async def handle_calendar_callback(callback_data, *, query: types.CallbackQuery, user_id) -> Union[date, QuestFunc]:
    """Return date or exception for turning/reiniting calendar."""
    try:
        _date = calendar.handle_callback(user_id, callback_data)
    except NotInitedException:
        await query.answer('Попробуйте еще раз')
        return QuestFunc(_reinit_calendar)

    if _date is None:
        return QuestFunc(_turn_calendar)
    return _date


@CurrentObjects.decorate
async def _reinit_calendar(*, msg: types.Message):
    keyboard = inline_funcs.make_calendar()
    await msg.edit_reply_markup(keyboard)


@CurrentObjects.decorate
async def _turn_calendar(*, msg: types.Message):
    keyboard = calendar.get_keyboard()
    await msg.edit_reply_markup(keyboard)
