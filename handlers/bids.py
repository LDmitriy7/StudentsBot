from aiogram import types

import functions as funcs
from datatypes import Chat, Prefixes
from filters import QueryPrefix
from keyboards import inline_funcs
from loader import bot, dp, users_db


@dp.callback_query_handler(QueryPrefix(Prefixes.PICK_BID_))
async def pick_bid(query: types.CallbackQuery, payload: str):
    """Приглашает обоих пользователей в чат."""
    bid = await users_db.get_bid_by_id(payload)
    client_id = bid.client_id
    worker_id = bid.worker_id

    await query.answer('Создание чатов займет некоторое время...', show_alert=True)
    chats = await funcs.create_and_save_chats(client_id, worker_id, bid.project_id)

    async def send_invite_msg(user_id: int, chat: Chat):
        text = 'Проект принят, перейдите в чат по ссылке'
        keyboard = inline_funcs.link_button('Перейти в чат', chat.link)
        if user_id == query.from_user.id:
            await query.message.edit_text(text, reply_markup=keyboard)
        else:
            await bot.send_message(user_id, text, reply_markup=keyboard)

    await send_invite_msg(client_id, chats.client_chat)
    await send_invite_msg(worker_id, chats.worker_chat)
