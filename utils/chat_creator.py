import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import ChatAdminRights
from telethon.tl.functions.messages import EditChatAdminRequest

api_id = 2034926
api_hash = '9046c41d3e17fd1b3eaed6352662773d'


async def create_chat(app):
    """Return chat_id, chat_link"""
    user = await app.get_entity("@test2_bot2_bot")
    res = await app(CreateChatRequest(title="Комната", users=[user]))

    chat_id = -res.updates[1].participants.chat_id
    await app(EditChatAdminRequest(chat_id, user, True))

    link = await app(ExportChatInviteRequest(chat_id))
    return chat_id, link.link


async def create_pair_chats():
    """Возвращает user_chat, worker_chat, user_link, worker_link"""
    async with TelegramClient('utils/account', api_id, api_hash) as app:
        user_chat, user_link = await create_chat(app)
        worker_chat, worker_link = await create_chat(app)
        return user_chat, worker_chat, user_link, worker_link


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(create_pair_chats())
    print(result)
