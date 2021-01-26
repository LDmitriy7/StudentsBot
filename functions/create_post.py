from aiogram import types
from aiogram.dispatcher import FSMContext

from typing import Union
from keyboards import inline_kb
from config import MAIN_CHANNEL, MAIN_POST_URL, MEDIA_CHANNEL, MEDIA_POST_URL
from loader import calendar
from questions.misc import HandleException
from utils.inline_calendar import NotInitedException
from datetime import date
from texts import templates


async def get_photo_post_url(msg: types.Message, state: FSMContext):
    """Отправляет все фото из хранилища в медиа-группу, возвращает ссылку на пост"""
    user_data = await state.get_data()
    photo_ids = user_data.get('photo_ids', [])

    if photo_ids:
        photos = [types.InputMediaPhoto(p) for p in photo_ids]
        group = types.MediaGroup(photos)

        post_ids = await msg.bot.send_media_group(MEDIA_CHANNEL, group)
        post_id = post_ids[0].message_id
        post_url = MEDIA_POST_URL.format(post_id)
    else:
        post_url = None

    return post_url


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
    """Return post, post_url, post_data"""
    post_data = await state.get_data()
    text = templates.form_post_text(post_data)
    post = await msg.bot.send_message(MAIN_CHANNEL, text)  # отправка в канал
    post_url = MAIN_POST_URL.format(post.message_id)
    post_data['post_url'] = post_url
    return post, post_url, post_data
