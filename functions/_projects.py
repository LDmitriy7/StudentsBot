"""Contain funcs for sending invitations and projects."""
from typing import List

from aiogram.dispatcher.currents import CurrentObjects
from aiogram.utils.exceptions import BadRequest

import functions.common as funcs
from data_types import data_classes, ProjectStatuses, UserRoles
from keyboards import inline_funcs
from loader import bot, users_db
from texts import templates

__all__ = ['send_projects', 'send_project_invitation',
           'send_chat_link_to_worker', 'start_project_update']


async def get_project_keyboard(project: data_classes.Project, pick_btn, del_btn,
                               client_chat_btns: bool, worker_chat_btns: bool):
    """Возращает инлайн-клавиатуру для проекта."""
    has_files = bool(project.data.files)
    can_be_deleted = bool(del_btn and project.status == ProjectStatuses.ACTIVE)
    can_be_reposted = bool(project.post_url and project.status == ProjectStatuses.ACTIVE)

    if client_chat_btns:
        chats = await users_db.get_chats_by_project(project.id)
        chats_links = [c.link for c in chats if c.user_role == UserRoles.client]
    elif worker_chat_btns:
        chats = await users_db.get_chats_by_project(project.id)
        chats_links = [c.link for c in chats if c.user_role == UserRoles.worker]
    else:
        chats_links = []

    return inline_funcs.ForProject(
        project.id,
        pick_btn=pick_btn,
        del_btn=can_be_deleted,
        files_btn=has_files,
        chat_links=chats_links,
        repost_btn=can_be_reposted
    )


@CurrentObjects.decorate
async def send_projects(projects: List[data_classes.Project],
                        with_note=False,
                        pick_btn=False,
                        del_btn=False,
                        client_chat_btns=False,
                        worker_chat_btn=False,
                        *, chat_id):
    """Отправить все проекты, используя шаблон.
    Добавить к каждому заметку, файлы и кнопки, если они выбраны и доступны."""

    for p in projects:
        text = templates.form_post_text(p.status, p.data, with_note)
        keyboard = await get_project_keyboard(p, pick_btn, del_btn, client_chat_btns, worker_chat_btn)
        await bot.send_message(chat_id, text, reply_markup=keyboard)


async def send_project_invitation(client_name: str, worker_id: int, chat_link: str) -> bool:
    """Try to send invitation to worker, return Message or HandleException."""
    text = f'Заказчик ({client_name}) предложил вам личный проект'
    keyboard = inline_funcs.link_button('Перейти в чат', chat_link)
    try:
        await bot.send_message(worker_id, text, reply_markup=keyboard)
        return True
    except BadRequest:
        return False


#
# @CurrentObjects.decorate
# async def send_personal_project(worker_id: int, worker_chat_link: str, *,
#                                 user_name, chat_id) -> bool:
#     """Try to send project to worker, return True on success."""
#
#     result = await send_project_invitation(user_name, worker_id, worker_chat_link)
#     if result is False:  # распространяем исключение
#         return False
#
#     keyboard = inline_funcs.link_button('Перейти в чат', worker_chat_link)
#     await bot.send_message(chat_id, 'Проект отправлен', reply_markup=Main())
#     await bot.send_message(chat_id, 'Ожидайте исполнителя в чате', reply_markup=keyboard)
#     return True


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
