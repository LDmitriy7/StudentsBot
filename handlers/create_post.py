"""Все для диалога: создание поста в канале."""
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import inline_kb, markup
from questions.create_post import CreatePostConv
from questions.misc import HandleException
from loader import calendar, users_db, dp
from functions.create_post import handle_calendar_callback, get_photo_post_url
from functions.common import get_file_obj
from texts.templates import form_post_text


# from config import MEDIA_CHANNEL, MEDIA_POST_URL
# from create_post.misc import get_photo_post_url, handle_calendar_callback, send_post
# from middlewares.misc import HandleException


@dp.message_handler(text='Создать пост ➕')
async def entry_create_post(msg: types.Message):
    return CreatePostConv, {'status': 'Активен'}


@dp.callback_query_handler(text=inline_kb.work_type_btns, state=CreatePostConv.work_type)
async def process_work_type(query: types.CallbackQuery):
    await query.answer()
    return {'work_type': query.data}


@dp.message_handler(state=CreatePostConv.subject)
async def process_subject(msg: types.Message):
    return {'subject': msg.text}


@dp.callback_query_handler(calendar.filter(), state=CreatePostConv.date)
async def process_date(query: types.CallbackQuery, callback_data: dict):
    result = await handle_calendar_callback(query, callback_data)

    if isinstance(result, HandleException):
        return result  # распространяем исключение

    await query.answer(f'Выбрано: {result}')
    return {'date': str(result)}


@dp.message_handler(state=CreatePostConv.description)
async def process_description(msg: types.Message):
    description = msg.text

    MIN_LEN, MAX_LEN = 15, 500

    if MIN_LEN < len(description) < MAX_LEN:
        return {'description': description}

    return HandleException(f'Ошибка, описание должно быть от {MIN_LEN} до {MAX_LEN} символов')


@dp.message_handler(state=CreatePostConv.price)
async def process_price(msg: types.Message):
    if msg.text == 'Пропустить':
        price = None
    elif msg.text.isdigit():
        price = int(msg.text)
    else:
        return HandleException('Ошибка, введите только число')

    return {'price': price}


@dp.message_handler(state=CreatePostConv.note)
async def process_note(msg: types.Message):
    note = None if msg.text == 'Пропустить' else msg.text
    return {'note': note}


@dp.message_handler(content_types=['photo', 'document'], state=CreatePostConv.files)
async def process_file(msg: types.Message):
    file_obj = get_file_obj(msg)
    return {'files': [file_obj]}, HandleException()


@dp.message_handler(text=['Готово', 'Сбросить выбор'], state=CreatePostConv.files)
async def process_file_finish(msg: types.Message):
    if msg.text == 'Сбросить выбор':
        return {'files': []}, HandleException('Теперь выбирайте заново')


@dp.message_handler(text='Отправить проект', state=CreatePostConv.confirm)
async def exit_create_post(msg: types.Message, state: FSMContext):
    post, post_url, post_data = await send_post(msg, state)  # отправка поста
#     project_id = await mongo_db.add_project(msg.from_user.id, post_data)  # сохранение в базу
#     pick_project_kb = await inline_kb.pick_post_project(project_id)
#     await post.edit_reply_markup(pick_project_kb)  # добавялем кнопку к посту
#     text = f'<a href="{post_url}">Проект</a> успешно создан'
#
#     await msg.answer(text, reply_markup=markup.main_kb)
#     await state.finish()  # finish conversation in any case
