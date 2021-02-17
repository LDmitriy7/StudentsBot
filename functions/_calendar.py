"""Contain funcs for work with inline calendar."""
from datetime import date
from typing import Union

from aiogram import types

from data_types import HandleException
from keyboards import inline_funcs
from loader import calendar
from utils.inline_calendar import NotInitedException
from subfuncs import decorators as current

__all__ = ['handle_calendar_callback']


@current.set_query
async def handle_calendar_callback(callback_data, query: types.CallbackQuery = None) -> Union[date, HandleException]:
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
