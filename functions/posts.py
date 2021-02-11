from typing import Tuple

from aiogram import types

import datatypes
from config import MAIN_CHANNEL, MAIN_POST_URL
from keyboards import inline_funcs
from loader import bot
from texts import templates

__all__ = ['send_post', 'add_post_keyboard', 'delete_post']


async def send_post(project_status: str, post_data: datatypes.ProjectData) -> Tuple[types.Message, str]:
    """Send post to channel. Return post_obj and post_url."""
    text = templates.form_post_text(project_status, post_data)
    post_obj = await bot.send_message(MAIN_CHANNEL, text)
    post_url = MAIN_POST_URL.format(post_obj.message_id)
    return post_obj, post_url


async def add_post_keyboard(post: types.Message, project_id: str, post_data: datatypes.ProjectData):
    """Добавляет к посту кнопки "Взять проект" и "Посмотреть файлы" (если имеются)."""
    has_files = bool(post_data.files)
    keyboard = inline_funcs.for_project(project_id, pick_btn=True, files_btn=has_files)
    await post.edit_reply_markup(keyboard)


async def delete_post(post_url: str):
    """Удаляет пост из канала, если передана ссылка."""
    if post_url:
        post_id = post_url.split('/')[-1]
        await bot.delete_message(MAIN_CHANNEL, post_id)
