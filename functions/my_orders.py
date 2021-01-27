from aiogram import types

from keyboards import inline_func
from loader import users_db, bot
from config import MAIN_CHANNEL
from texts import templates
from typing import List


async def get_project(msg: types.Message):
    """Return project and project_id."""
    project_id = inline_func.get_payload(msg.text)
    project = await users_db.get_project_by_id(project_id)
    return project, project_id


async def delete_post(project: dict):
    post_url: str = project.get('post_url')
    if post_url:  # удаляем из канала
        post_id = int(post_url.split('/')[-1])
        await bot.delete_message(MAIN_CHANNEL, post_id)
