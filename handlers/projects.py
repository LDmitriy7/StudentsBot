"""Обработка данных с кнопок под проектами: посмотреть файлы, удалить проект."""

from aiogram import types
from aiogram.contrib.questions import QuestText

import functions as funcs
import keyboards as KB
from data_types import ProjectStatuses
from loader import dp, users_db


@dp.callback_query_handler(button=KB.ForProject.REPOST, state='*')
async def repost_project(query: types.CallbackQuery, suffix: str):
    throttle_rate = 60 * 60
    if not await dp.throttle(repost_project.__name__, rate=throttle_rate, no_error=True):
        text = f'Вы можете обновлять ваши проекты не чаще раза в {throttle_rate // 60} мин.'
        await query.answer(text, show_alert=True)
        return

    project = await users_db.get_project_by_id(suffix)
    await funcs.delete_post(project.post_url)
    post = await funcs.send_post(project.id, project.data, project.status)
    await users_db.update_project_post_url(project.id, post.url)
    await query.answer('Проект переопубликован')


@dp.message_handler(button=KB.ForProject.FILES, state='*')
async def send_files(suffix: str):
    """Отправляет все файлы к проекту."""
    project = await users_db.get_project_by_id(suffix)
    if project:
        await funcs.send_files(project.data.files)
    else:
        return 'Этот проект уже удален'


@dp.callback_query_handler(button=KB.ForProject.DELETE, state='*')
async def del_project(suffix: str):
    """Просит потвердить удаление проекта."""
    text = 'Вы точно хотите удалить проект?'
    keyboard = KB.DelProject(suffix)
    return QuestText(text, keyboard)


@dp.callback_query_handler(button=KB.DelProject.DEL_PROJECT, state='*')
async def total_del_project(msg: types.Message, user_id: int, suffix: str):
    """Удаляет проект, если он имеет активный статус и принадлежит юзеру."""
    project = await users_db.get_project_by_id(suffix)

    if project is None:
        text = 'Этот проект уже удален'
    elif project.status == ProjectStatuses.ACTIVE and project.client_id == user_id:
        text = 'Проект удален'
        await funcs.delete_post(project.post_url)  # удаляем пост, если есть ссылка
        await users_db.delete_project_by_id(suffix)
    else:
        text = 'Не могу удалить этот проект.'
    await msg.edit_text(text)
