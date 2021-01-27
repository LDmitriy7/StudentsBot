"""Обрабатывает данные с кнопок для взаимодействия с проектами."""
from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from functions import common as cfuncs
from keyboards import inline_func
from keyboards import markup
from loader import dp, users_db
from states import Projects
from texts import templates
from questions.registration import RegistrationConv


@dp.message_handler(CommandStart(inline_func.GET_FILES_PATTERN))
async def send_files(msg: types.Message):
    project_id = inline_func.get_payload(msg.text)
    project = await users_db.get_project_by_id(project_id)
    if project:
        files = project['data'].get('files', [])
        for file in files:
            await cfuncs.send_file(msg.from_user.id, *file)
    else:
        await msg.answer('Этот проект уже удален')


@dp.message_handler(CommandStart(inline_func.SEND_BID_PATTERN))
async def ask_bid_text(msg: types.Message):
    """Запрашивает текст для заявки у исполнителя."""
    account = await users_db.get_account_by_id(msg.from_user.id)
    profile = account.get('profile') if account else None
    if not profile:
        await msg.answer('Сначала пройдите регистрацию')
        return RegistrationConv

    project_id = inline_func.get_payload(msg.text)
    project = await users_db.get_project_by_id(project_id)
    if project:
        await Projects.ask_bid_text.set()
        await msg.answer('Отправьте текст для заявки:', reply_markup=markup.cancel_kb)
        return {'project_id': project_id, 'client_id': project['client_id']}
    else:
        await msg.answer('Этот проект уже удален')


@dp.callback_query_handler(text_startswith=inline_func.DEL_PROJECT_PREFIX)
async def del_project(query: types.CallbackQuery):
    """Просит потвердить удаление проекта."""
    project_id = inline_func.get_payload(query.data)
    text = 'Вы точно хотите удалить проект?'
    keyboard = inline_func.delete_project(project_id)
    await query.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(text_startswith=inline_func.TOTAL_DEL_PROJECT_PREFIX)
async def total_del_project(query: types.CallbackQuery):
    """Удаляет проект, если он имеет активный статус и принадлежит юзеру."""
    project_id = inline_func.get_payload(query.data)
    project = await users_db.get_project_by_id(project_id)

    if project is None:
        text = 'Этот проект уже удален.'
    elif project['status'] == 'Активен' and project['client_id'] == query.from_user.id:
        post_url: str = project.get('post_url')
        await cfuncs.delete_post(post_url)  # удаляем из канала
        text = 'Проект удален'
    else:
        text = 'Не могу удалить этот проект.'

    await users_db.delete_project_by_id(project_id)
    await query.message.answer(text)


@dp.callback_query_handler(text_startswith=inline_func.GET_PROJECT_PREFIX)
async def get_project(query: types.CallbackQuery):
    project_id = inline_func.get_payload(query.data)
    project = await users_db.get_project_by_id(project_id)
    if project:
        text = templates.form_post_text(project['status'], project['data'], with_note=True)
        has_files = bool(project['data'].get('files'))
        keyboard = await inline_func.for_project(project_id, files_button=has_files)
        await query.message.answer(text, reply_markup=keyboard)
    else:
        await query.answer('Этот проект уже удален')
