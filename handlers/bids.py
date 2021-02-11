from aiogram import types

from filters import QueryPrefix
from keyboards import inline_funcs
from loader import bot, dp, users_db
from datatypes import Chat, Prefixes
from utils.chat_creator import create_pair_chats


@dp.callback_query_handler(QueryPrefix(Prefixes.PICK_BID_))
async def pick_bid(query: types.CallbackQuery, payload: str):
    """Приглашает обоих пользователей в чат."""
    bid = await users_db.get_bid_by_id_test(payload)
    project_id = bid.project_id
    client_id = bid.client_id
    worker_id = bid.worker_id

    chats = await create_pair_chats('Нора1', project_id, client_id, worker_id)

    async def send_invite_msg(user_id: int, chat: Chat):
        text = 'Проект принят, перейдите в чат по ссылке'
        keyboard = inline_funcs.link_button('Перейти в чат', chat.link)
        if user_id == query.from_user.id:
            await query.message.edit_text(text, reply_markup=keyboard)
        else:
            await bot.send_message(user_id, text, reply_markup=keyboard)
        await users_db.add_chat(chat)  # сохранение чата

    await send_invite_msg(client_id, chats.client_chat)
    await send_invite_msg(worker_id, chats.worker_chat)
