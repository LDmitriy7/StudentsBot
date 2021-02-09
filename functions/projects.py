from typing import List

from aiogram import types
from type_classes import ProjectData, Project
from keyboards import inline_funcs
from loader import users_db
from texts import templates


async def send_projects(
        msg: types.Message, projects: List[dict], with_note=False,
        pick_btn=False, del_btn=False, client_chat_btn=False, worker_chat_btn=False
):
    """Отправляет в ответ проекты по списку (добавляет кнопку файлов, если они есть)."""
    assert not (client_chat_btn and worker_chat_btn)

    for p in projects:
        post_data = p['data']
        status = p['status']
        project_id = str(p['_id'])

        text = templates.form_post_text(status, post_data, with_note)
        has_files = bool(post_data.get('files'))
        can_delete = del_btn and status == 'Активен'

        if client_chat_btn:
            chat_link = p.get('client_chat_link')
        elif worker_chat_btn:
            chat_link = p.get('worker_chat_link')
        else:
            chat_link = None

        keyboard = inline_funcs.for_project(
            project_id,
            pick_btn=pick_btn,
            del_btn=can_delete,
            files_btn=has_files,
            chat_link=chat_link
        )
        await msg.answer(text, reply_markup=keyboard)


async def save_project(project_data: dict, client_id: int, worker_id: int) -> str:
    """Сохраняет активный проект в базу, возращает его id."""
    project_data = ProjectData(**project_data)
    project = Project(client_id, project_data, 'Активен', worker_id=worker_id)
    project_id = await users_db.add_project_test(project)  # сохранение проекта
    return project_id
