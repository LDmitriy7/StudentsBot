"""Модуль для генерации парных чатов с общим ботом и админ-аккаунтом.
Требует наличие telethon-сессии в папке."""

from typing import Tuple

from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest, EditChatAdminRequest, ExportChatInviteRequest

from config import API_HASH, API_ID, LINKED_BOT
from type_classes import Chat, PairChats


async def create_chat(app, title: str) -> Tuple[int, str]:
    """Return chat_id, chat_link"""
    user = await app.get_entity(LINKED_BOT)
    result = await app(CreateChatRequest(title=title, users=[user]))

    chat_id = -result.updates[1].participants.chat_id
    chat_link = await app(ExportChatInviteRequest(chat_id))
    await app(EditChatAdminRequest(chat_id, user, True))

    return chat_id, chat_link.link


async def create_pair_chats(title: str, project_id: str, client_id: int, worker_id: int) -> PairChats:
    """Create 2 pair chats for anonymous conversation."""
    async with TelegramClient('utils/account', API_ID, API_HASH) as app:
        cchat_id, cchat_link = await create_chat(app, title)
        wchat_id, wchat_link = await create_chat(app, title)

        client_chat = Chat(cchat_id, project_id, 'client', client_id, cchat_link, wchat_id)
        worker_chat = Chat(wchat_id, project_id, 'worker', worker_id, wchat_link, cchat_id)
        return PairChats(client_chat, worker_chat)

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     r = loop.run_until_complete(create_pair_chats('Тест1'))
#     print(r)
