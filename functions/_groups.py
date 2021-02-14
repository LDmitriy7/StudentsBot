from typing import Optional

from aiogram import types

import datatypes
from datatypes import PairChats, Update, ProjectStatuses, UserRoles
from keyboards import inline_funcs
from loader import bot, users_db
from utils.chat_creator import create_pair_chats

__all__ = ['create_and_save_groups', 'get_chat_of_update', 'get_project_status', 'get_user_role',
           'get_project_for_chat', 'get_group_keyboard']

GROUP_NUM = 0


async def create_and_save_groups(client_id: int, worker_id: int, project_id: str) -> PairChats:
    """Создает чаты с порядковым номером в названии и сохраняет их."""
    global GROUP_NUM
    GROUP_NUM += 1

    await bot.send_chat_action(client_id, 'typing')
    pair_chats = await create_pair_chats(f'Нора #{GROUP_NUM}', project_id, client_id, worker_id)
    client_chat, worker_chat = pair_chats.client_chat, pair_chats.worker_chat

    await users_db.add_chat(client_chat)
    await users_db.add_chat(worker_chat)
    return pair_chats


def get_chat_of_update(update: Update) -> types.Chat:
    """Return chat of update (Message or CallbackQuery)."""
    return update.chat if isinstance(update, types.Message) else update.message.chat


async def get_project_status(chat: types.Chat) -> Optional[str]:
    """Return status of linked project or None."""
    project = await get_project_for_chat(chat)
    status = project.status if project else None
    return status


async def get_user_role(chat: types.Chat) -> Optional[str]:
    """Return user role in chat or None."""
    chat = await users_db.get_chat_by_id(chat.id)
    return chat.user_role if chat else None


async def get_project_for_chat(chat: types.Chat) -> Optional[datatypes.Project]:
    """Get linked project for chat or None."""
    chat = await users_db.get_chat_by_id(chat.id)
    try:
        project = await users_db.get_project_by_id(chat.project_id)
    except AttributeError:
        project = None
    return project


async def get_group_keyboard(chat: types.Chat) -> inline_funcs.GroupMenuKeyboard:
    """Создает меню для группы, основываясь на статусе проекта и роли юзера."""
    pstatus = await get_project_status(chat)
    user_role = await get_user_role(chat)

    call_admin, offer_price, confirm_project, feedback = True, False, False, False

    if pstatus == ProjectStatuses.ACTIVE and user_role == UserRoles.WORKER:
        offer_price = True
    elif pstatus == ProjectStatuses.IN_PROGRESS and user_role == UserRoles.CLIENT:
        confirm_project = True
    elif pstatus == ProjectStatuses.COMPLETED and user_role == UserRoles.CLIENT:
        feedback = True
    return inline_funcs.group_menu(call_admin, offer_price, confirm_project, feedback)
