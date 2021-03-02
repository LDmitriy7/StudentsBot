"""Модуль для генерации парных чатов с общим ботом и админ-аккаунтом.
Требует наличие telethon-сессии в папке."""

from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest, EditChatAdminRequest, DeleteChatUserRequest

from config import API_HASH, API_ID, CONV_BOT_USERNAME, BOT_USERNAME


async def create_chat(title: str) -> int:
    async with TelegramClient('utils/account', API_ID, API_HASH) as app:
        conv_bot = await app.get_entity(CONV_BOT_USERNAME)
        main_bot = await app.get_entity(BOT_USERNAME)
        result = await app(CreateChatRequest(title=title, users=[conv_bot, main_bot]))

        chat_id = -result.updates[1].participants.chat_id
        await app(EditChatAdminRequest(chat_id, conv_bot, True))
        await app(EditChatAdminRequest(chat_id, main_bot, True))
        return chat_id

#
# async def test():
#     async with TelegramClient('account', API_ID, API_HASH) as app:
#         app: TelegramClient
#         # main_bot = await app.get_entity(BOT_USERNAME)
#
#         for i in await app.get_dialogs():
#             chat = getattr(i, 'entity')
#             # me = await app.get_me(True)
#             if 2 < getattr(chat, 'participants_count', 0) < 10:
#                 # print(chat)
#                 print(chat.id, end=', ')
#                 # try:
#                 #     await app.get_
#                 #     await app(EditChatAdminRequest(chat.id, main_bot.id, True))
#                 # except Exception as e:
#             # print(chat.id)
#             # if chat.id != 1300392478:
#             #     await app(DeleteChatUserRequest(chat.id, me))


import asyncio

# asyncio.run(test())

# ids = [
#
# ]
# for chat_id in ids:
#     coro = test(chat_id)
#     print(chat_id)
#     asyncio.run(coro)
