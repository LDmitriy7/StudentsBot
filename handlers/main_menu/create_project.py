"""Все для диалога: создание поста в канале."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestFunc

import functions as funcs
import keyboards as KB
from loader import calendar, dp
from questions import CreateProjectConv as States


@dp.callback_query_handler(button=KB.work_types.BUTTONS, state=States.work_type)
async def process_work_type(data):
    return UpdateData({'work_type': data})


@dp.message_handler(state=States.subject)
async def process_subject(text):
    return UpdateData({'subject': text})


@dp.callback_query_handler(calendar.filter(), state=States.date)
async def process_date(query: types.CallbackQuery, callback_data: dict):
    handle_result = await funcs.handle_calendar_callback(callback_data)

    if isinstance(handle_result, QuestFunc):
        return handle_result  # распространяем исключение

    await query.answer(f'Выбрано: {handle_result}')
    return UpdateData({'date': str(handle_result)})


@dp.message_handler(state=States.description)
async def process_description(text):
    min_len, max_len = 15, 500
    if min_len < len(text) < max_len:
        return UpdateData({'description': text})
    return f'Ошибка, описание должно быть от {min_len} до {max_len} символов'


@dp.message_handler(state=States.price)
async def process_price(text):
    if text == KB.miss.MISS:
        price = None
    elif text.isdigit():
        price = int(text)
    else:
        return 'Ошибка, введите только число'
    return UpdateData({'price': price})


@dp.message_handler(state=States.note)
async def process_note(text):
    note = None if text == KB.miss.MISS else text
    return UpdateData({'note': note})


@dp.message_handler(content_types=['photo', 'document'], state=States.files)
async def process_file():
    file_obj = await funcs.get_file_tuple()
    return UpdateData(extend_data={'files': file_obj}, new_state=None)


@dp.message_handler(button=[KB.ready.READY, KB.ready.START_OVER], state=States.files)
async def process_file_finish(text):
    if text == KB.ready.START_OVER:
        return UpdateData(delete_keys='files', new_state=None), 'Теперь отправляйте заново'
    return UpdateData(extend_data={'files': []})
