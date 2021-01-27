from datetime import date
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext

from config import MAIN_CHANNEL, MAIN_POST_URL
from keyboards import inline_kb
from loader import calendar
from questions.misc import HandleException
from texts import templates
from utils.inline_calendar import NotInitedException


async def handle_calendar_callback(query: types.CallbackQuery, callback_data) -> Union[date, HandleException]:
    try:
        date = calendar.handle_callback(query.from_user.id, callback_data)
    except NotInitedException:
        await query.answer('Попробуйте еще раз')
        return HandleException(_reinit_calendar)

    if date is None:
        return HandleException(_turn_calendar)

    return date


async def _reinit_calendar(msg: types.Message):
    keyboard = inline_kb.get_calendar()
    await msg.edit_reply_markup(keyboard)


async def _turn_calendar(msg: types.Message):
    keyboard = calendar.get_keyboard()
    await msg.edit_reply_markup(keyboard)


async def send_post(msg: types.Message, state: FSMContext):
    """Return post_obj, post_url, post_data"""
    post_data = await state.get_data()
    text = templates.form_post_text(post_data)
    post = await msg.bot.send_message(MAIN_CHANNEL, text)  # отправка в канал
    post_url = MAIN_POST_URL.format(post.message_id)
    post_data['post_url'] = post_url
    return post, post_url, post_data


async def add_post_keyboard(post: types.Message, project_id: str, with_files: bool):
    keyboard = await inline_kb.project_kb(project_id, files=with_files)
    await post.edit_reply_markup(keyboard)
