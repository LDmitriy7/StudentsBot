from aiogram import types
from aiogram.dispatcher import FSMContext

from functions.bids import remove_button
from keyboards import inline_func, markup
from loader import bot, dp, users_db
from questions.misc import HandleException
from states import Projects
from texts import templates
from utils.chat_creator import create_pair_chats


@dp.message_handler(state=Projects.ask_bid_text)
async def send_bid(msg: types.Message, state: FSMContext):
    """Отправялет заявку заказчику."""
    bid_text = msg.text

    if not 15 < len(bid_text) < 500:
        return HandleException('Ошибка, текст заявки должен быть от 15 до 500 символов')

    worker_id = msg.from_user.id
    bid_data = await state.get_data()
    project_id, client_id = bid_data['project_id'], bid_data['client_id']

    text = templates.form_bid_text('http://test.com', 'Имя', bid_text)
    bid_id = await users_db.add_bid(client_id, project_id, worker_id, bid_text)
    keyboard = inline_func.for_bid(project_id, bid_id)

    await bot.send_message(client_id, text, reply_markup=keyboard)  # отправка заказчику
    await msg.answer('Заявка отправлена', reply_markup=markup.main_kb)
    await state.finish()


@dp.callback_query_handler(text_startswith=inline_func.PICK_BID_PREFIX)
async def pick_bid(query: types.CallbackQuery):
    """Приглашает обоих пользователей в чат."""
    client_id = query.from_user.id
    bid_id = inline_func.get_payload(query.data)
    await remove_button(query, 1)  # удаляем кнопку приглашения
    await bot.send_chat_action(client_id, 'typing')

    bid = await users_db.get_bid_by_id(bid_id)
    project_id, worker_id = bid['project_id'], bid['worker_id']

    pair_chats = await create_pair_chats('Нора1')
    client_chat: dict = pair_chats.client_chat
    worker_chat: dict = pair_chats.worker_chat

    # сохранение чатов
    await users_db.add_chat(project_id, **client_chat, user_id=client_id)
    await users_db.add_chat(project_id, **worker_chat, user_id=worker_id)

    client_text = f'Приглашение отправлено, ожидайте в чате {client_chat["link"]}'
    worker_text = f'Заказчик пригласил вас в чат {worker_chat["link"]}'

    await bot.send_message(client_id, client_text)
    await bot.send_message(worker_id, worker_text)
