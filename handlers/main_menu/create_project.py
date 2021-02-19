"""Все для диалога: создание поста в канале."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestFunc

import functions as funcs
from keyboards.inline_plain import WorkTypeKeyboard
from loader import calendar, dp
from questions import CreateProjectConv as States


@dp.callback_query_handler(text=WorkTypeKeyboard.WORK_TYPE_BTNS, state=States.work_type)
async def process_work_type(query: types.CallbackQuery):
    return UpdateData({'work_type': query.data})


@dp.message_handler(state=States.subject)
async def process_subject(msg: types.Message):
    return UpdateData({'subject': msg.text})


@dp.callback_query_handler(calendar.filter(), state=States.date)
async def process_date(query: types.CallbackQuery, callback_data: dict):
    handle_result = await funcs.handle_calendar_callback(callback_data)
    if isinstance(handle_result, QuestFunc):
        return handle_result  # распространяем исключение
    await query.answer(f'Выбрано: {handle_result}')
    return UpdateData({'date': str(handle_result)})


@dp.message_handler(state=States.description)
async def process_description(msg: types.Message):
    min_len, max_len = 15, 500
    if min_len < len(msg.text) < max_len:
        return UpdateData({'description': msg.text})
    return f'Ошибка, описание должно быть от {min_len} до {max_len} символов'


@dp.message_handler(state=States.price)
async def process_price(msg: types.Message):
    if msg.text == 'Пропустить':
        price = None
    elif msg.text.isdigit():
        price = int(msg.text)
    else:
        return 'Ошибка, введите только число'
    return UpdateData({'price': price})


@dp.message_handler(state=States.note)
async def process_note(msg: types.Message):
    note = None if msg.text == 'Пропустить' else msg.text
    return UpdateData({'note': note})


@dp.message_handler(content_types=['photo', 'document'], state=States.files)
async def process_file(msg: types.Message):
    file_obj = funcs.get_file_tuple(msg)
    return UpdateData(extend_data={'files': file_obj}, new_state=None)


@dp.message_handler(text=['Готово', 'Начать заново'], state=States.files)
async def process_file_finish(msg: types.Message):
    if msg.text == 'Начать заново':
        return UpdateData(delete_keys='files', new_state=None), 'Теперь отправляйте заново'
    return UpdateData(extend_data={'files': []})
