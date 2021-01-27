"""Модуль для генерации парных чатов с общим ботом и админ-аккаунтом.
Требует наличие telethon-сессии в папке."""

import asyncio
from collections import namedtuple
from typing import Tuple

from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest, EditChatAdminRequest, ExportChatInviteRequest

from config import API_HASH, API_ID, LINKED_BOT

PairChats = namedtuple('PairChats', ['client_chat', 'worker_chat'])


async def create_chat(app, title: str) -> Tuple[int, str]:
    """Return chat_id, chat_link"""
    user = await app.get_entity(LINKED_BOT)
    result = await app(CreateChatRequest(title=title, users=[user]))

    chat_id = -result.updates[1].participants.chat_id
    chat_link = await app(ExportChatInviteRequest(chat_id))
    await app(EditChatAdminRequest(chat_id, user, True))

    return chat_id, chat_link.link


async def create_pair_chats(title: str) -> PairChats:
    """Return PairChats: dicts(chat_id, chat_type, link, pair_id)"""
    async with TelegramClient('utils/account', API_ID, API_HASH) as app:
        cchat_id, cchat_link = await create_chat(app, title)
        wchat_id, wchat_link = await create_chat(app, title)

        client_chat = {
            'chat_id': cchat_id,
            'chat_type': 'client',
            'link': cchat_link,
            'pair_id': wchat_id
        }
        worker_chat = {
            'chat_id': wchat_id,
            'chat_type': 'worker',
            'link': wchat_link,
            'pair_id': cchat_id
        }

        return PairChats(client_chat, worker_chat)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    r = loop.run_until_complete(create_pair_chats('Тест1'))
    print(r)
