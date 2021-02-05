from aiogram import types

from functions.bids import remove_button
from keyboards import inline_funcs
from keyboards.inline_funcs import Prefixes
from filters import QueryPrefix
from loader import bot, dp, users_db
from texts import templates
from utils.chat_creator import create_pair_chats


@dp.callback_query_handler(QueryPrefix(Prefixes.PICK_BID_))
async def pick_bid(query: types.CallbackQuery, payload: str):
    """Приглашает обоих пользователей в чат."""
    client_id = query.from_user.id
    await remove_button(query, 1)  # удаляем кнопку приглашения
    await bot.send_chat_action(client_id, 'typing')

    bid = await users_db.get_bid_by_id(payload)
    project_id, worker_id = bid['project_id'], bid['worker_id']

    pair_chats = await create_pair_chats('Нора1')
    client_chat: dict = pair_chats.client_chat
    worker_chat: dict = pair_chats.worker_chat

    # сохранение чатов
    await users_db.add_chat(project_id, **client_chat, user_id=client_id)
    await users_db.add_chat(project_id, **worker_chat, user_id=worker_id)

    client_text = f'Приглашение отправлено, ждите автора в чате'
    worker_text = f'Заказчик проекта пригласил вас в чат'
    client_kb = inline_funcs.link_button('Перейти в чат', client_chat['link'])
    worker_kb = inline_funcs.link_button('Перейти в чат', worker_chat['link'])

    await bot.send_message(client_id, client_text, reply_markup=client_kb)
    await bot.send_message(worker_id, worker_text, reply_markup=worker_kb)


@dp.callback_query_handler(QueryPrefix(Prefixes.GET_PROJECT_))
async def get_project(query: types.CallbackQuery, payload: str):
    project = await users_db.get_project_by_id(payload)
    if project:
        text = templates.form_post_text(project['status'], project['data'], with_note=True)
        has_files = bool(project['data'].get('files'))
        keyboard = inline_funcs.for_project(payload, files_btn=has_files)
        await query.message.answer(text, reply_markup=keyboard)
    else:
        await query.answer('Этот проект уже удален')
