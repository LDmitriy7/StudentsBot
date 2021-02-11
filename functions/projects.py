from typing import List

from aiogram import types

import datatypes
import functions as funcs
from keyboards import inline_funcs
from texts import templates


async def send_projects(
        msg: types.Message, projects: List[datatypes.Project], with_note=False,
        pick_btn=False, del_btn=False, client_chat_btn=False, worker_chat_btn=False
):
    """Отправляет в ответ проекты по списку (добавляет кнопку файлов, если они есть)."""
    assert not (client_chat_btn and worker_chat_btn)

    for p in projects:
        post_data = p.data
        status = p.status
        project_id = p.id

        text = templates.form_post_text(status, post_data, with_note)
        has_files = bool(post_data.files)
        can_delete = del_btn and status == 'Активен'

        if client_chat_btn:
            chat_link = funcs.get_chat_link(p.client_chat_id)
        elif worker_chat_btn:
            chat_link = funcs.get_chat_link(p.worker_chat_id)
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
