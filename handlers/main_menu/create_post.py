"""Все для диалога: создание поста в канале."""
from aiogram import types
from aiogram.dispatcher import FSMContext

import datatypes as datatypes
import functions._calendar
import functions.files
import functions.posts
from functions import common as cfuncs
from functions import create_post as funcs
from keyboards import markup
from keyboards.inline_plain import WorkTypeKeyboard
from loader import calendar, dp, users_db
from questions.create_post import CreatePostConv as States
from questions.misc import HandleException


@dp.message_handler(text='Создать пост ➕')
async def entry_create_post(msg: types.Message):
    return States  # входим в беседу


@dp.callback_query_handler(text=WorkTypeKeyboard.WORK_TYPE_BTNS, state=States.work_type)
async def process_work_type(query: types.CallbackQuery):
    await query.answer()
    return {'work_type': query.data}


@dp.message_handler(state=States.subject)
async def process_subject(msg: types.Message):
    return {'subject': msg.text}


@dp.callback_query_handler(calendar.filter(), state=States.date)
async def process_date(query: types.CallbackQuery, callback_data: dict):
    handle_result = await functions._calendar.handle_calendar_callback(query, callback_data)
    if isinstance(handle_result, HandleException):
        return handle_result  # распространяем исключение
    await query.answer(f'Выбрано: {handle_result}')
    return {'date': str(handle_result)}


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
    file_obj = functions.files.get_file_obj(msg)
    return {'files': [file_obj]}, HandleException()


@dp.message_handler(text=['Готово', 'Начать заново'], state=States.files)
async def process_file_finish(msg: types.Message):
    if msg.text == 'Начать заново':
        return {'files': ()}, HandleException('Теперь выбирайте заново')
    return {'files': []}


@dp.message_handler(text='Отправить проект', state=States.confirm)
async def exit_create_post(msg: types.Message, state: FSMContext):
    udata = await state.get_data()
    project_data = datatypes.ProjectData(**udata)
    project = datatypes.Project(project_data, msg.from_user.id)

    post_obj, post_url = await functions.posts.send_post(project.status, project_data)
    project.post_url = post_url
    project_id = await users_db.add_project(project)

    text = f'<a href="{post_url}">Проект</a> успешно создан'
    await functions.posts.add_post_keyboard(post_obj, project_id, project_data)
    await msg.answer(text, reply_markup=markup.main_kb)
