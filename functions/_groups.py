from typing import Optional

from aiogram import types

from data_types import ProjectStatuses, UserRoles
from data_types.data_classes import PairChats, Project
from keyboards import inline_funcs
from loader import bot, users_db
from subfuncs import decorators as current
from utils.chat_creator import create_pair_chats

__all__ = ['create_and_save_groups', 'get_project_status', 'get_user_role',
           'get_project_for_chat', 'get_group_keyboard']

GROUP_NUM = 0


async def create_and_save_groups(client_id: int, worker_id: int, project_id: str) -> PairChats:
    """Создает парные группы с порядковым номером в названии и сохраняет их."""
    global GROUP_NUM
    GROUP_NUM += 1

    await bot.send_chat_action(client_id, 'typing')
    pair_chats = await create_pair_chats(f'Нора #{GROUP_NUM}', project_id, client_id, worker_id)

    await users_db.add_chat(pair_chats.client_chat)
    await users_db.add_chat(pair_chats.worker_chat)
    return pair_chats


@current.set_chat
async def get_project_for_chat(chat: types.Chat = None) -> Optional[Project]:
    """Get linked project for chat or None."""
    chat = await users_db.get_chat_by_id(chat.id)
    try:
        project = await users_db.get_project_by_id(chat.project_id)
    except AttributeError:
        project = None
    return project


@current.set_chat
async def get_project_status(chat: types.Chat = None) -> Optional[str]:
    """Return status of linked project or None."""
    project = await get_project_for_chat(chat=chat)
    return project.status if project else None


@current.set_chat
async def get_user_role(chat: types.Chat = None) -> Optional[str]:
    """Return user role in chat or None."""
    chat = await users_db.get_chat_by_id(chat.id)
    return chat.user_role if chat else None


@current.set_chat
async def get_group_keyboard(chat: types.Chat = None) -> inline_funcs.GroupMenuKeyboard:
    """Создает меню для группы, основываясь на статусе проекта и роли юзера."""
    pstatus = await get_project_status(chat)
    user_role = await get_user_role(chat)

    call_admin = True
    offer_price = pstatus == ProjectStatuses.ACTIVE and user_role == UserRoles.WORKER
    confirm_project = pstatus == ProjectStatuses.IN_PROGRESS and user_role == UserRoles.CLIENT
    feedback = pstatus == ProjectStatuses.COMPLETED and user_role == UserRoles.CLIENT

    return inline_funcs.group_menu(call_admin, offer_price, confirm_project, feedback)
