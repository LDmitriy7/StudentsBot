"""Обработка данных с кнопок под проектами: посмотреть файлы, взять проект, удалить проект."""

from aiogram import types

import functions as funcs
from datatypes import Prefixes, ProjectStatuses
from filters import DeepLinkPrefix, QueryPrefix
from keyboards import inline_funcs
from loader import dp, users_db


@dp.message_handler(DeepLinkPrefix(Prefixes.GET_FILES_))
async def send_files(msg: types.Message, payload: str):
    """Отправляет все файлы к проекту."""
    project = await users_db.get_project_by_id(payload)
    if project:
        await funcs.send_files(msg.from_user.id, project.data.files)
    else:
        await msg.answer('Этот проект уже удален')


@dp.callback_query_handler(QueryPrefix(Prefixes.DEL_PROJECT_))
async def del_project(query: types.CallbackQuery, payload: str):
    """Просит потвердить удаление проекта."""
    text = 'Вы точно хотите удалить проект?'
    keyboard = inline_funcs.del_project(payload)
    await query.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(QueryPrefix(Prefixes.TOTAL_DEL_PROJECT_))
async def total_del_project(query: types.CallbackQuery, payload: str):
    """Удаляет проект, если он имеет активный статус и принадлежит юзеру."""
    project = await users_db.get_project_by_id(payload)

    if project is None:
        text = '<b>Этот проект уже удален</b>'
    elif project.status == ProjectStatuses.ACTIVE and project.client_id == query.from_user.id:
        text = '<b>Проект удален</b>'
        await funcs.delete_post(project.post_url)  # удаляем пост, если есть ссылка
        await users_db.delete_project_by_id(payload)
    else:
        text = '<b>Не могу удалить этот проект.</b>'
    await query.message.edit_text(text)
