from typing import Optional

from aiogram.dispatcher.currents import CurrentObjects
from aiogram.utils.exceptions import TelegramAPIError

import functions as funcs
import keyboards as KB
from data_types import ProjectStatuses, UserRoles, data_classes
from loader import users_db, bot
from utils import create_chat

__all__ = ['get_project_status', 'get_user_role', 'create_and_save_groups',
           'get_project_for_chat', 'get_group_keyboard']

GROUP_NUM = 0


async def _check_chat_freedom(chat_id) -> Optional[int]:
    try:
        pstatus = await funcs.get_project_status(chat_id=chat_id)
        if pstatus in [ProjectStatuses.COMPLETED, ProjectStatuses.REVIEWED, None]:
            members_count = await bot.get_chat_members_count(chat_id)
            if members_count <= 3:
                return True
    except TelegramAPIError:
        return False


async def _get_pair_chat_ids(title: str) -> list[int]:
    chat_ids = []

    for chat in await users_db.get_all_chats():
        if await _check_chat_freedom(chat.id):
            chat_ids.append(chat.id)
        if len(chat_ids) >= 2:
            break
    else:
        while len(chat_ids) < 2:
            chat_id = await create_chat(title)
            chat_ids.append(chat_id)

    return chat_ids


async def create_and_save_groups(client_id: int, worker_id: int, project_id: str) -> data_classes.PairChats:
    """Создает парные группы с порядковым номером в названии и сохраняет их."""
    global GROUP_NUM
    GROUP_NUM += 1

    await bot.send_chat_action(client_id, 'typing')
    cchat_id, wchat_id = await _get_pair_chat_ids(f'Нора #{GROUP_NUM}')

    cchat_link = await bot.export_chat_invite_link(cchat_id)
    wchat_link = await bot.export_chat_invite_link(wchat_id)

    cchat = data_classes.Chat(project_id, UserRoles.client, client_id, cchat_link, wchat_id, cchat_id)
    wchat = data_classes.Chat(project_id, UserRoles.worker, worker_id, wchat_link, cchat_id, wchat_id)
    await users_db.update_chat(cchat_id, cchat)
    await users_db.update_chat(wchat_id, wchat)

    return data_classes.PairChats(cchat, wchat)


@CurrentObjects.decorate
async def get_project_for_chat(*, chat_id: int) -> Optional[data_classes.Project]:
    """Get linked project for chat or None."""
    try:
        chat = await users_db.get_chat_by_id(chat_id)
        project = await users_db.get_project_by_id(chat.project_id)
    except AttributeError:
        project = None
    return project


@CurrentObjects.decorate
async def get_project_status(*, chat_id: int) -> Optional[str]:
    """Return status of linked project or None."""
    project = await get_project_for_chat(chat_id=chat_id)
    return project.status if project else None


@CurrentObjects.decorate
async def get_user_role(*, chat_id: int) -> Optional[str]:
    """Return user role in chat or None."""
    chat = await users_db.get_chat_by_id(chat_id)
    return chat.user_role if chat else None


@CurrentObjects.decorate
async def get_group_keyboard(*, chat_id: int) -> KB.GroupMenu:
    """Создает меню для группы, основываясь на статусе проекта и роли юзера."""
    pstatus = await get_project_status(chat_id=chat_id)
    user_role = await get_user_role(chat_id=chat_id)

    call_admin = True
    offer_price = pstatus == ProjectStatuses.ACTIVE and user_role == UserRoles.worker
    confirm_project = pstatus == ProjectStatuses.IN_PROGRESS and user_role == UserRoles.client
    feedback = pstatus == ProjectStatuses.COMPLETED and user_role == UserRoles.client
    return KB.group_menu(call_admin, offer_price, confirm_project, feedback)
