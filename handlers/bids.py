from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText

import functions as funcs
import texts
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
        return UpdateData(new_state=RegistrationConv), 'Сначала пройдите регистрацию'

    if not project:
        return '<b>Этот проект уже удален</b>'

    if msg.from_user.id == project.client_id:
        return '<b>Вы не можете взять свой проект</b>'

    return UpdateData({'project_id': payload, 'client_id': project.client_id}, new_state=SendBidConv)


@dp.message_handler(state=SendBidConv.bid_text)
async def send_bid(msg: types.Message):
    """Отправялет заявку заказчику."""
    if msg.text.startswith('/start'):
        return 'Ошибка, отправьте текст для заявки'

    bid = await funcs.save_bid()
    full_bid_text = await funcs.get_worker_bid_text(bid.project_id)
    keyboard = inline_funcs.for_bid(bid.id)
    await bot.send_message(bid.client_id, full_bid_text, reply_markup=keyboard)
    return UpdateData(on_conv_exit=QuestText('Заявка отправлена', markup.main_kb))


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


@dp.callback_query_handler(QueryPrefix(Prefixes.PICK_PROJECT_), state='*')
async def pick_project(query: types.CallbackQuery, payload: str):
    project = await users_db.get_project_by_id(payload)

    if not project:
        await query.answer('Этот проект уже удален')
        return

    if query.from_user.id == project.client_id:
        await query.answer('Вы не можете сами принять проект')
        return

    account = await users_db.get_account_by_id(query.from_user.id)
    if not (account and account.profile):
        await query.answer(texts.registration, show_alert=True)
        return

    await query.edit_inline_message('<b>Поиск свободных чатов...</b>')
    chats = await funcs.create_and_save_groups(project.client_id, query.from_user.id, payload)

    client_text = f'Исполнитель ({query.from_user.full_name}) взял ваш проект'
    worker_text = 'Вы взяли персональный проект, перейдите в чат'
    await funcs.send_chat_link(project.client_id, client_text, chats.client_chat.link)
    await funcs.send_chat_link(query.from_user.id, worker_text, chats.worker_chat.link)
    await query.edit_inline_message('<b>Проект принят, бот отправил ссылки в чаты лично</b>')
