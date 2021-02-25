from typing import Optional

from data_types import ProjectStatuses, UserRoles
from data_types.data_classes import PairChats, Project
from keyboards import inline_funcs
from loader import bot, users_db
from subfuncs.currents2 import Currents
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


@Currents.set
async def get_project_for_chat(*, chat_id: int) -> Optional[Project]:
    """Get linked project for chat or None."""
    try:
        chat = await users_db.get_chat_by_id(chat_id)
        project = await users_db.get_project_by_id(chat.project_id)
    except AttributeError:
        project = None
    return project


@Currents.set
async def get_project_status(*, chat_id: int) -> Optional[str]:
    """Return status of linked project or None."""
    project = await get_project_for_chat(chat_id=chat_id)
    return project.status if project else None


@Currents.set
async def get_user_role(*, chat_id: int) -> Optional[str]:
    """Return user role in chat or None."""
    chat = await users_db.get_chat_by_id(chat_id)
    return chat.user_role if chat else None


@Currents.set
async def get_group_keyboard(*, chat_id: int) -> inline_funcs.GroupMenu:
    """Создает меню для группы, основываясь на статусе проекта и роли юзера."""
    pstatus = await get_project_status(chat_id=chat_id)
    user_role = await get_user_role(chat_id=chat_id)

    CALL_ADMIN = True
    OFFER_PRICE = pstatus == ProjectStatuses.ACTIVE and user_role == UserRoles.WORKER
    CONFIRM_PROJECT = pstatus == ProjectStatuses.IN_PROGRESS and user_role == UserRoles.client
    FEEDBACK = pstatus == ProjectStatuses.COMPLETED and user_role == UserRoles.client

    exclude_btns = {key: None for key, value in locals().items() if not value and key.isupper()}
    return inline_funcs.GroupMenu(**exclude_btns)
