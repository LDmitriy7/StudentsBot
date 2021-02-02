from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import bot
from config import MAIN_CHANNEL, MAIN_POST_URL
from keyboards import inline_func
from texts import templates
from typing import Tuple


async def send_post(post_data: dict) -> Tuple[types.Message, str]:
    """Send post to channel. Add post_url to post_data. Return post_obj and post_url."""
    status = post_data['status']
    text = templates.form_post_text(status, post_data)
    post_obj = await bot.send_message(MAIN_CHANNEL, text)
    post_url = MAIN_POST_URL.format(post_obj.message_id)
    post_data['post_url'] = post_url
    return post_obj, post_url


async def add_post_keyboard(post: types.Message, project_id: str, post_data: dict):
    """Добавляет к посту кнопки "Взять проект" и "Посмотреть файлы" (если имеются)."""

    has_files = bool(post_data.get('files'))

    keyboard = await inline_func.for_project(
        project_id,
        pick_btn=True,
        files_btn=has_files
    )
    await post.edit_reply_markup(keyboard)
