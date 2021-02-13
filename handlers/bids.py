from aiogram import types
from aiogram.dispatcher import FSMContext

import datatypes
import functions as funcs
from datatypes import Prefixes
from filters import DeepLinkPrefix, QueryPrefix
from keyboards import inline_funcs, markup
from loader import bot, dp, users_db
from questions import RegistrationConv
from questions.misc import HandleException
from states import Projects as States


@dp.message_handler(DeepLinkPrefix(Prefixes.SEND_BID_))
async def ask_bid_text(msg: types.Message, payload: str):
    """Запрашивает текст для заявки у исполнителя или отправляет на регистрацию."""
    worker_id = msg.from_user.id
    account = await users_db.get_account_by_id(worker_id)
    profile = account and account.profile or None
    project = await users_db.get_project_by_id(payload)

    if not profile:
        await msg.answer('Сначала пройдите регистрацию')
        return RegistrationConv

    if not project:
        await msg.answer('<b>Этот проект уже удален</b>')
        return

    if worker_id == project.client_id:
        await msg.answer('<b>Вы не можете взять свой проект</b>')
        return

    await States.ask_bid_text.set()
    await msg.answer('Отправьте текст для заявки:', reply_markup=markup.cancel_kb)
    return {'project_id': payload, 'client_id': project.client_id}


@dp.message_handler(state=States.ask_bid_text)
async def send_bid(msg: types.Message, state: FSMContext):
    """Отправялет заявку заказчику."""
    bid_text = msg.text
    worker_id = msg.from_user.id

    if bid_text.startswith('/start'):
        return HandleException('Ошибка, отправьте текст для заявки')

    bid_data = await state.get_data()
    client_id, project_id = bid_data['client_id'], bid_data['project_id']

    bid_id = await funcs.save_bid(client_id, project_id, worker_id, bid_text)
    full_bid_text = await funcs.get_worker_bid_text(worker_id, project_id, bid_text)
    print(full_bid_text)
    keyboard = inline_funcs.for_bid(bid_id)

    await bot.send_message(client_id, full_bid_text, reply_markup=keyboard)  # отправка заказчику
    await msg.answer('Заявка отправлена', reply_markup=markup.main_kb)
    await state.finish()


@dp.callback_query_handler(QueryPrefix(Prefixes.PICK_BID_))
async def pick_bid(query: types.CallbackQuery, payload: str):
    """Принять заявку, пригласить обоих пользователей в чат."""
    bid = await users_db.get_bid_by_id(payload)
    client_id, worker_id = bid.client_id, bid.worker_id

    await query.answer('Поиск свободных чатов...', show_alert=True)
    chats = await funcs.create_and_save_chats(client_id, worker_id, bid.project_id)

    async def send_invite_msg(text: str, user_id: int, chat: datatypes.Chat):
        keyboard = inline_funcs.link_button('Перейти в чат', chat.link)
        if user_id == query.from_user.id:
            await query.message.edit_text(text, reply_markup=keyboard)
        else:
            await bot.send_message(user_id, text, reply_markup=keyboard)

    client_text = 'Вы приняли заявку, ожидайте исполнителя в чате'
    worker_text = f'Заказчик ({query.from_user.full_name}) принял вашу заявку, перейдите в чат'
    await send_invite_msg(client_text, client_id, chats.client_chat)
    await send_invite_msg(worker_text, worker_id, chats.worker_chat)
