"""Contain funcs for sending invitations and projects."""
from typing import List, Optional, Tuple

from aiogram.utils.exceptions import BadRequest

import datatypes
from datatypes import ProjectStatuses
import functions.common as funcs
from config import MAIN_CHANNEL, MAIN_POST_URL
from keyboards import inline_funcs, markup
from loader import bot
from questions.misc import HandleException
from texts import templates

__all__ = ['send_projects', 'send_project_invitation', 'send_personal_project', 'send_post_to_channel',
           'send_chat_link_to_worker']


async def send_projects(
        chat_id: int, projects: List[datatypes.Project], with_note=False,
        pick_btn=False, del_btn=False, client_chat_btn=False, worker_chat_btn=False
):
    """Отправляет проекты по списку (добавляет кнопки, если они выбраны и доступны)."""
    assert not (client_chat_btn and worker_chat_btn)

    for p in projects:
        has_files = bool(p.data.files)
        can_delete = del_btn and p.status == ProjectStatuses.ACTIVE
        text = templates.form_post_text(p.status, p.data, with_note)

        if client_chat_btn:
            chat_link = await funcs.get_chat_link(p.client_chat_id)
        elif worker_chat_btn:
            chat_link = await funcs.get_chat_link(p.worker_chat_id)
        else:
            chat_link = None

        keyboard = inline_funcs.for_project(
            p.id,
            pick_btn=pick_btn,
            del_btn=can_delete,
            files_btn=has_files,
            chat_link=chat_link
        )
        await bot.send_message(chat_id, text, reply_markup=keyboard)


async def send_project_invitation(client_name: str, worker_id: int, chat_link: str) -> Optional[HandleException]:
    """Try to send invitation to worker, return Message or HandleException."""
    text = f'Заказчик ({client_name}) предложил вам личный проект'
    keyboard = inline_funcs.link_button('Перейти в чат', chat_link)
    try:
        await bot.send_message(worker_id, text, reply_markup=keyboard)
    except BadRequest:
        return HandleException('Не могу отправить этому исполнителю')


async def send_personal_project(chat_id: int, client_name: str, worker_id: int, worker_chat_link: str) -> bool:
    """Try to send project to worker, return True on success."""
    result = await send_project_invitation(client_name, worker_id, worker_chat_link)
    if isinstance(result, HandleException):  # распространяем исключение
        return False

    keyboard = inline_funcs.link_button('Перейти в чат', worker_chat_link)
    await bot.send_message(chat_id, 'Проект отправлен', reply_markup=markup.main_kb)
    await bot.send_message(chat_id, 'Ожидайте исполнителя в чате', reply_markup=keyboard)
    return True


#####

async def send_post_to_channel(
        project_id: str, project_status: str, post_data: datatypes.ProjectData
) -> str:
    """Send post to channel. Return post_url."""
    text = templates.form_post_text(project_status, post_data)
    has_files = bool(post_data.files)
    keyboard = inline_funcs.for_project(project_id, pick_btn=True, files_btn=has_files)

    post_obj = await bot.send_message(MAIN_CHANNEL, text, reply_markup=keyboard)
    post_url = MAIN_POST_URL.format(post_obj.message_id)
    return post_url


async def send_chat_link_to_worker(client_name: str, worker_id: int, worker_chat_link: str):
    """Send invite chat link"""
    text = f'Заказчик ({client_name}) предложил вам личный проект'
    keyboard = inline_funcs.link_button('Перейти в чат', worker_chat_link)
    await bot.send_message(worker_id, text, reply_markup=keyboard)
