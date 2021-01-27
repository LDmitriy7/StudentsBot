import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from functions.bids import get_full_bid
from keyboards import inline_kb, markup
from states import MiscStates
from texts import templates
# from common.texts.templates import bid_template
from loader import bot, dp, users_db

PICK_PROJECT_PATTERN = re.compile(f'{inline_kb.PICK_PROJECT_PREFIX}[0-9a-f]+')
GET_FILES_PATTERN = re.compile(f'{inline_kb.GET_FILES_PREFIX}[0-9a-f]+')


@dp.message_handler(CommandStart(PICK_PROJECT_PATTERN))
async def ask_bid_text(msg: types.Message, state: FSMContext):
    payload = msg.text.split()[-1]
    project_id = payload.replace(inline_kb.PICK_PROJECT_PREFIX, '')

    await MiscStates.ask_bid_text.set()
    await state.update_data(
        project_id=project_id,
        worker_id=msg.from_user.id,
        worker_name=msg.from_user.full_name,
    )
    await msg.answer('Отправьте текст для заявки:', reply_markup=markup.cancel_kb)


@dp.message_handler(state=MiscStates.ask_bid_text)
async def send_bid(msg: types.Message, state: FSMContext):
    bid_text = msg.text

    if not 15 < len(bid_text) < 500:
        await msg.answer('Ошибка, текст заявки должен быть от 15 до 500 символов')
        return

    bid_data, worker_name, post_url, note = await get_full_bid(state)
    bid_id = await users_db.add_bid(**bid_data, text=bid_text)  # сохранение заявки

    bid_text_data = dict(
        worker_url='',
        worker_nickname=worker_name,
        post_url=post_url,
        bid_text=bid_text,
        note=note,
    )
    bid_text_result = templates.form_bid_text(bid_text_data)
    keyboard = inline_kb.answer_bid(bid_id)
    await bot.send_message(bid_data['user_id'], bid_text_result, reply_markup=keyboard)  # отправка заказчику

    await msg.answer('Заявка отправлена', reply_markup=markup.main_kb)
    await state.finish()

# @dp.callback_query_handler(text='refuse:bid')
# async def refuse_bid(query: types.CallbackQuery):
#     """Удаляет сообщение с заявкой"""
#     msg = query.message
#     await msg.edit_text('<b> * Заявка отклонена</b>')
#
#
# @dp.callback_query_handler(text_startswith='pick:bid:')
# async def pick_bid(query: types.CallbackQuery):
#     """Приглашает обоих пользователей в чат."""
#     msg = query.message
#     reply_markup = msg.reply_markup
#     reply_markup.inline_keyboard.pop(0)  # удаляем кнопку приглашения
#
#     await bot.send_chat_action(query.from_user.id, 'typing')
#
#     project_id, chats_dict = await get_pair_chats(query)  # создание чатов
#
#     user_id, worker_id = chats_dict['users']
#     user_link, worker_link = chats_dict['links']
#     chats = chats_dict['chats']
#
#     await mongo_db.add_chats_to_project(project_id, *chats)  # сохранение чатов
#     pchats_db.set(chats[0], chats[1])  # добавялем в redis
#     pchats_db.set(chats[1], chats[0])  # добавялем в redis
#
#     if query.from_user.id == user_id:  # if query was sent by client
#         user_text = f'Приглашение отправлено, ожидайте в чате {user_link}'
#         worker_text = f'Заказчик пригласил вас в чат {worker_link}'
#     else:  # if query was sent by author
#         user_text = f'Автор принял заказ, ожидайте в чате {user_link}'
#         worker_text = f'Ожидайте в чате {worker_link}'
#
#     await bot.send_message(user_id, user_text)
#     await bot.send_message(worker_id, worker_text)
#     await msg.edit_reply_markup(reply_markup)
#
