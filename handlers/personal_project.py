"""Все для диалога: создание поста в канале."""
from aiogram import types
from aiogram.dispatcher import FSMContext

from functions.common import get_file_obj
from functions.create_post import add_post_keyboard, handle_calendar_callback
from functions.personal_project import send_project
from keyboards import inline_kb, markup
from loader import calendar, dp, users_db
from questions.misc import HandleException
from questions.personal_project import PersonalProjectConv


@dp.message_handler(text='Личный проект 🤝')
async def entry_create_post(msg: types.Message):
    return PersonalProjectConv, {'status': 'Активен'}


@dp.callback_query_handler(text=inline_kb.work_type_btns, state=PersonalProjectConv.work_type)
async def process_work_type(query: types.CallbackQuery):
    await query.answer()
    return {'work_type': query.data}


@dp.message_handler(state=PersonalProjectConv.subject)
async def process_subject(msg: types.Message):
    return {'subject': msg.text}


@dp.callback_query_handler(calendar.filter(), state=PersonalProjectConv.date)
async def process_date(query: types.CallbackQuery, callback_data: dict):
    result = await handle_calendar_callback(query, callback_data)

    if isinstance(result, HandleException):
        return result  # распространяем исключение

    await query.answer(f'Выбрано: {result}')
    return {'date': str(result)}


@dp.message_handler(state=PersonalProjectConv.description)
async def process_description(msg: types.Message):
    description = msg.text

    MIN_LEN, MAX_LEN = 15, 500

    if MIN_LEN < len(description) < MAX_LEN:
        return {'description': description}

    return HandleException(f'Ошибка, описание должно быть от {MIN_LEN} до {MAX_LEN} символов')


@dp.message_handler(state=PersonalProjectConv.price)
async def process_price(msg: types.Message):
    if msg.text == 'Пропустить':
        price = None
    elif msg.text.isdigit():
        price = int(msg.text)
    else:
        return HandleException('Ошибка, введите только число')

    return {'price': price}


@dp.message_handler(state=PersonalProjectConv.note)
async def process_note(msg: types.Message):
    note = None if msg.text == 'Пропустить' else msg.text
    return {'note': note}


@dp.message_handler(content_types=['photo', 'document'], state=PersonalProjectConv.files)
async def process_file(msg: types.Message):
    file_obj = get_file_obj(msg)
    return {'files': [file_obj]}, HandleException()


@dp.message_handler(text=['Готово', 'Сбросить выбор'], state=PersonalProjectConv.files)
async def process_file_finish(msg: types.Message):
    if msg.text == 'Сбросить выбор':
        return {'files': []}, HandleException('Теперь выбирайте заново')


@dp.message_handler(state=PersonalProjectConv.worker)
async def process_worker(msg: types.Message):
    if msg.text.isdigit():
        worker = int(msg.text)
        if 10 ** 5 < worker < 10 ** 15:
            return {'worker': worker}
    return HandleException('Неверный ID, попросите ID у исполнителя')


@dp.message_handler(text='Отправить проект', state=PersonalProjectConv.confirm)
async def exit_create_post(msg: types.Message, state: FSMContext):
    result = await send_project(msg, state)  # отправка сообщения
    if isinstance(result, HandleException):  # распространяем исключение
        return result

    worker, post_msg, post_data = result
    project_id = await users_db.add_project(msg.from_user.id, post_data)  # сохранение проекта
    has_files = bool(post_data.get('files'))
    await add_post_keyboard(post_msg, project_id, has_files)

    text1 = 'Проект успешно создан и отправлен'
    await msg.answer(text1, reply_markup=markup.main_kb)
    await state.finish()  # finish conversation in any case
