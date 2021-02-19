from aiogram import types
from aiogram.contrib.middlewares.conversation import HandleException, NewData, NewState

import functions as funcs
from data_types import Prefixes
from filters import DeepLinkPrefix, QueryPrefix
from keyboards import inline_funcs, markup
from loader import dp, users_db, bot
from questions import RegistrationConv, SendBidConv


@dp.message_handler(DeepLinkPrefix(Prefixes.SEND_BID_))
async def ask_bid_text(msg: types.Message, payload: str):
    """Запрашивает текст для заявки у исполнителя."""
    account = await users_db.get_account_by_id(msg.from_user.id)
    project = await users_db.get_project_by_id(payload)

    if not (account and account.profile):
        await msg.answer('Сначала пройдите регистрацию')
        return NewState(RegistrationConv)

    if not project:
        await msg.answer('<b>Этот проект уже удален</b>')
        return

    if msg.from_user.id == project.client_id:
        await msg.answer('<b>Вы не можете взять свой проект</b>')
        return

    new_data = NewData({'project_id': payload, 'client_id': project.client_id})
    return new_data, NewState(SendBidConv)


@dp.message_handler(state=SendBidConv.bid_text)
async def send_bid(msg: types.Message):
    """Отправялет заявку заказчику."""
    if msg.text.startswith('/start'):
        return HandleException('Ошибка, отправьте текст для заявки')

    bid = await funcs.save_bid()
    full_bid_text = await funcs.get_worker_bid_text(bid.project_id)
    keyboard = inline_funcs.for_bid(bid.id)

    await bot.send_message(bid.client_id, full_bid_text, reply_markup=keyboard)
    await msg.answer('Заявка отправлена', reply_markup=markup.main_kb)


@dp.callback_query_handler(QueryPrefix(Prefixes.PICK_BID_), state='*')
async def pick_bid(query: types.CallbackQuery, payload: str):
    """Принять заявку: пригласить обоих пользователей в чат."""
    bid = await users_db.get_bid_by_id(payload)
    await query.message.edit_text('<b>Поиск чата, ожидайте...</b>')
    chats = await funcs.create_and_save_groups(bid.client_id, bid.worker_id, bid.project_id)

    client_text = 'Вы приняли заявку, ожидайте исполнителя в чате'
    worker_text = f'Заказчик ({query.from_user.full_name}) принял вашу заявку, перейдите в чат'
    await funcs.send_chat_link(bid.client_id, client_text, chats.client_chat.link)
    await funcs.send_chat_link(bid.worker_id, worker_text, chats.worker_chat.link)
    return HandleException()


@dp.callback_query_handler(QueryPrefix(Prefixes.PICK_PROJECT_), state='*')
async def pick_project(query: types.CallbackQuery, payload: str):
    project = await users_db.get_project_by_id(payload)
    client_id, worker_id = project.client_id, query.from_user.id

    if worker_id == client_id:
        await query.answer('Вы не можете сами принять проект')
        return

    account = await users_db.get_account_by_id(worker_id)
    if not (account and account.profile):
        await query.answer('Сначала пройдите регистрацию в боте', markup.main_kb)
        await bot.send_message(worker_id, 'Загляните в меню исполнителя')
        return

    await query.answer('Поиск свободных чатов...', show_alert=True)
    chats = await funcs.create_and_save_groups(client_id, worker_id, payload)

    async def send_invite_msg(text: str, user_id: int, chat: Chat):
        keyboard = inline_funcs.link_button('Перейти в чат', chat.link)
        await bot.send_message(user_id, text, reply_markup=keyboard)

    client_text = f'Исполнитель ({query.from_user.full_name}) взял ваш проект'
    worker_text = 'Вы взяли персональный проект, перейдите в чат'
    await send_invite_msg(client_text, client_id, chats.client_chat)
    await send_invite_msg(worker_text, worker_id, chats.worker_chat)

    new_text = '<b>Проект принят, бот отправил ссылки в чаты лично</b>'
    await bot.edit_message_text(new_text, inline_message_id=query.inline_message_id)
