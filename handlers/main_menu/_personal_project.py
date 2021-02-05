"""Все для диалога: создание поста в канале."""
from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import DeepLinkPrefix
from functions import common as cfuncs
from functions import personal_project as funcs
from keyboards.inline_funcs import Prefixes
from keyboards.inline_plain import WorkTypeKeyboard
from keyboards import inline_funcs, inline_plain, markup
from loader import bot, calendar, dp, users_db
from questions.misc import HandleException
from questions.personal_project import PersonalProjectConv as States
from utils.chat_creator import create_pair_chats
from texts import main as texts


# вход в создание проекта

@dp.message_handler(text='Личный проект 🤝')
async def ask_user_role(msg: types.Message):
    await msg.answer(texts.start_personal_project, reply_markup=markup.personal_project)


@dp.message_handler(text='Я заказчик')
async def entry_create_post(msg: types.Message):
    await msg.answer('Сначала заполните проект')
    return States  # входим в диалог


@dp.message_handler(text='Я исполнитель')
async def choose_client_chat(msg: types.Message):
    text = 'Выберите <b>заказчика</b> из списка своих чатов'
    keyboard = inline_plain.offer_project_to_client
    await msg.answer(text, reply_markup=keyboard)


@dp.message_handler(DeepLinkPrefix(Prefixes.OFFER_PROJECT_))
async def entry_create_post_with_worker(msg: types.Message, payload: str):
    worker_id = int(payload)
    if msg.from_user.id == worker_id:
        return HandleException('<b>Вы сами не можете заполнить проект</b>')
    return States, {'worker_id': worker_id}  # входим в диалог с заданнным исполнителем


# заполнение проекта

@dp.callback_query_handler(text=WorkTypeKeyboard.WORK_TYPE_BTNS, state=States.work_type)
async def process_work_type(query: types.CallbackQuery):
    return {'work_type': query.data}


@dp.message_handler(state=States.subject)
async def process_subject(msg: types.Message):
    return {'subject': msg.text}


@dp.callback_query_handler(calendar.filter(), state=States.date)
async def process_date(query: types.CallbackQuery, callback_data: dict):
    result = await cfuncs.handle_calendar_callback(query, callback_data)

    if isinstance(result, HandleException):
        return result  # распространяем исключение

    await query.answer(f'Выбрано: {result}')
    return {'date': str(result)}


@dp.message_handler(state=States.description)
async def process_description(msg: types.Message):
    min_len, max_len = 15, 500
    description = msg.text
    if min_len < len(description) < max_len:
        return {'description': description}
    return HandleException(f'Ошибка, описание должно быть от {min_len} до {max_len} символов')


@dp.message_handler(state=States.price)
async def process_price(msg: types.Message):
    if msg.text == 'Пропустить':
        price = None
    elif msg.text.isdigit():
        price = int(msg.text)
    else:
        return HandleException('Ошибка, введите только число')
    return {'price': price}


@dp.message_handler(state=States.note)
async def process_note(msg: types.Message):
    note = None if msg.text == 'Пропустить' else msg.text
    return {'note': note}


@dp.message_handler(content_types=['photo', 'document'], state=States.files)
async def process_file(msg: types.Message):
    file_obj = cfuncs.get_file_obj(msg)
    return {'files': [file_obj]}, HandleException()


@dp.message_handler(text=['Готово', 'Начать заново'], state=States.files)
async def process_file_finish(msg: types.Message):
    if msg.text == 'Начать заново':
        return {'files': ()}, HandleException('Теперь выбирайте заново')
    return {'files': [], 'status': 'Активен'}

# @dp.message_handler(text='Отправить проект', state=States.confirm)
# async def send_personal_post(msg: types.Message, state: FSMContext):
#     post_data = await state.get_data()
#     client_id = msg.from_user.id
#     worker_id = post_data['worker_id']
#
#     post_msg = await funcs.send_project(msg.from_user.full_name, post_data)
#     if isinstance(post_msg, HandleException):  # распространяем исключение
#         return post_msg
#
#     project_id = await users_db.add_project(msg.from_user.id, post_data)  # сохранение проекта
#     await bot.send_chat_action(client_id, 'typing')
#
#     pair_chats = await create_pair_chats('Нора1')  # создание чатов
#     client_chat: dict = pair_chats.client_chat
#     worker_chat: dict = pair_chats.worker_chat
#
#     await users_db.add_chat(project_id, **client_chat, user_id=client_id)
#     await users_db.add_chat(project_id, **worker_chat, user_id=worker_id)
#     await funcs.add_post_keyboard(post_msg, worker_chat['link'])  # добавляем кнопку-приглашение
#
#     text1 = 'Проект успешно создан и отправлен'
#     keyboard1 = markup.main_kb
#     text2 = 'Ожидайте автора в чате'
#     keyboard2 = inline_funcs.link_button('Перейти в чат', client_chat['link'])
#     await msg.answer(text1, reply_markup=keyboard1)
#     await msg.answer(text2, reply_markup=keyboard2)
