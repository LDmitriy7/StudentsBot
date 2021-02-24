"""Contain funcs for sending invitations and projects."""
from typing import List

from aiogram import types
from aiogram.utils.exceptions import BadRequest

import functions.common as funcs
from data_types import data_classes, ProjectStatuses
from keyboards import inline_funcs, Main
from loader import bot, users_db
from subfuncs.currents2 import Currents
from texts import templates

__all__ = ['send_projects', 'send_project_invitation', 'send_personal_project',
           'send_chat_link_to_worker', 'start_project_update']


async def get_project_keyboard(project: data_classes.Project, pick_btn, del_btn, client_chat_btn, worker_chat_btn):
    """Возращает инлайн-клавиатуру для проекта."""
    has_files = bool(project.data.files)
    can_delete = del_btn and project.status == ProjectStatuses.ACTIVE

    if client_chat_btn:
        chat_link = await funcs.get_chat_link(project.client_chat_id)
    elif worker_chat_btn:
        chat_link = await funcs.get_chat_link(project.worker_chat_id)
    else:
        chat_link = None

    keyboard = inline_funcs.for_project(
        project.id,
        pick_btn=pick_btn,
        del_btn=can_delete,
        files_btn=has_files,
        chat_link=chat_link
    )
    return keyboard


@Currents.set
async def send_projects(projects: List[data_classes.Project], with_note=False,
                        pick_btn=False, del_btn=False, client_chat_btn=False, worker_chat_btn=False,
                        *, chat: types.Chat):
    """Отправляет проекты по списку (добавляет кнопки, если они выбраны и доступны)."""

    for p in projects:
        text = templates.form_post_text(p.status, p.data, with_note)
        keyboard = await get_project_keyboard(p, pick_btn, del_btn, client_chat_btn, worker_chat_btn)
        await bot.send_message(chat.id, text, reply_markup=keyboard)


async def send_project_invitation(client_name: str, worker_id: int, chat_link: str) -> bool:
    """Try to send invitation to worker, return Message or HandleException."""
    text = f'Заказчик ({client_name}) предложил вам личный проект'
    keyboard = inline_funcs.link_button('Перейти в чат', chat_link)
    try:
        await bot.send_message(worker_id, text, reply_markup=keyboard)
        return True
    except BadRequest:
        return False


@Currents.set
async def send_personal_project(worker_id: int, worker_chat_link: str, client_name: str = None, *,
                                chat: types.Chat) -> bool:
    """Try to send project to worker, return True on success."""

    if client_name is None:
        client_name = types.User.get_current().full_name

    result = await send_project_invitation(client_name, worker_id, worker_chat_link)
    if result is False:  # распространяем исключение
        return False

    keyboard = inline_funcs.link_button('Перейти в чат', worker_chat_link)
    await bot.send_message(chat.id, 'Проект отправлен', reply_markup=Main())
    await bot.send_message(chat.id, 'Ожидайте исполнителя в чате', reply_markup=keyboard)
    return True


async def send_chat_link_to_worker(client_name: str, worker_id: int, worker_chat_link: str):
    """Send invite chat link to worker."""
    text = f'Заказчик ({client_name}) предложил вам личный проект'
    keyboard = inline_funcs.link_button('Перейти в чат', worker_chat_link)
    await bot.send_message(worker_id, text, reply_markup=keyboard)


async def start_project_update(
        project_id: str, price: int, client_id: int, worker_id: int,
        client_chat_id: int, worker_chat_id: int
):
    """Update project and post after paying it."""
    amount = -price
    # обновить данные в базе
    await users_db.incr_balance(client_id, amount)
    await users_db.update_project_price(project_id, price)
    await users_db.update_project_worker(project_id, worker_id)
    await users_db.update_project_chats(project_id, client_chat_id, worker_chat_id)
    await users_db.update_project_status(project_id, ProjectStatuses.IN_PROGRESS)
    # обновить пост
    project = await users_db.get_project_by_id(project_id)
    await funcs.update_post(project_id, project.status, project.post_url, project.data)
