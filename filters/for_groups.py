from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import functions as funcs
from data_types import ProjectStatuses, UserRoles
from loader import users_db


async def find_pair_chat(*args) -> Union[dict, bool]:
    """Try to find a pair chat (group) and return it id ('pchat_id')."""
    chat = types.Chat.get_current()
    if chat.type == 'group':
        chat_obj = await users_db.get_chat_by_id(chat.id)
        if chat_obj:
            return {'pchat_id': chat_obj.pair_id}
    return False


class ProjectStatus(BoundFilter):
    key = 'pstatus'

    def __init__(self, pstatus: str):
        if pstatus not in ProjectStatuses.all():
            raise ValueError('Invalid project status.')
        self.pstatus = pstatus

    async def check(self, *args) -> bool:
        pstatus = await funcs.get_project_status()
        return pstatus == self.pstatus


class ChatUserRole(BoundFilter):
    key = 'user_role'

    def __init__(self, user_role: str):
        if user_role not in UserRoles.all():
            raise ValueError('Invalid chat\'s user role.')
        self.user_role = user_role

    async def check(self, *args) -> bool:
        user_role = await funcs.get_user_role()
        return user_role == self.user_role
