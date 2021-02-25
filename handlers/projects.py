"""Обработка данных с кнопок под проектами: посмотреть файлы, удалить проект."""

from aiogram import types

import functions as funcs
from data_types import Prefixes, ProjectStatuses
from keyboards import inline_funcs
from loader import dp, users_db
from aiogram.contrib.questions import QuestText


@dp.message_handler(cprefix=Prefixes.GET_FILES_, state='*')
async def send_files(payload: str):
    """Отправляет все файлы к проекту."""
    project = await users_db.get_project_by_id(payload)
    if project:
        await funcs.send_files(project.data.files)
    else:
        return 'Этот проект уже удален'


@dp.callback_query_handler(cprefix=Prefixes.DEL_PROJECT_, state='*')
async def del_project(payload: str):
    """Просит потвердить удаление проекта."""
    text = 'Вы точно хотите удалить проект?'
    keyboard = inline_funcs.del_project(payload)
    return QuestText(text, keyboard)


@dp.callback_query_handler(cprefix=Prefixes.TOTAL_DEL_PROJECT_, state='*')
async def total_del_project(msg: types.Message, user_id: int, payload: str):
    """Удаляет проект, если он имеет активный статус и принадлежит юзеру."""
    project = await users_db.get_project_by_id(payload)

    if project is None:
        text = '<b>Этот проект уже удален</b>'
    elif project.status == ProjectStatuses.ACTIVE and project.client_id == user_id:
        text = '<b>Проект удален</b>'
        await funcs.delete_post(project.post_url)  # удаляем пост, если есть ссылка
        await users_db.delete_project_by_id(payload)
    else:
        text = '<b>Не могу удалить этот проект.</b>'
    await msg.edit_text(text)
