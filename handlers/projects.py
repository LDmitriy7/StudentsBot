"""Обработка данных с кнопок под проектами: посмотреть файлы, взять проект, удалить проект."""

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import DeepLinkPrefix, QueryPrefix
from functions import bids as funcs
from functions import common as cfuncs
from keyboards import inline_funcs, markup
from keyboards.inline_funcs import Prefixes
from loader import bot, dp, users_db
from questions.misc import HandleException
from questions.registration import RegistrationConv
from states import Projects as States
from type_classes import Bid


@dp.message_handler(DeepLinkPrefix(Prefixes.GET_FILES_))
async def send_files(msg: types.Message, payload: str):
    """Отправляет все файлы к проекту."""
    project = await users_db.get_project_by_id(payload)
    if project:
        files = project['data'].get('files', [])
        for file in files:
            await cfuncs.send_file(msg.from_user.id, *file)
    else:
        await msg.answer('Этот проект уже удален')


@dp.callback_query_handler(QueryPrefix(Prefixes.DEL_PROJECT_))
async def del_project(query: types.CallbackQuery, payload: str):
    """Просит потвердить удаление проекта."""
    text = 'Вы точно хотите удалить проект?'
    keyboard = inline_funcs.del_project(payload)
    await query.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(QueryPrefix(Prefixes.TOTAL_DEL_PROJECT_))
async def total_del_project(query: types.CallbackQuery, payload: str):
    """Удаляет проект, если он имеет активный статус и принадлежит юзеру."""
    project = await users_db.get_project_by_id(payload)

    if project is None:
        text = '<b>Этот проект уже удален</b>'
    elif project['status'] == 'Активен' and project['client_id'] == query.from_user.id:
        text = '<b>Проект удален</b>'
        post_url = project.get('post_url')
        await cfuncs.delete_post(post_url)  # удаляем пост, если есть ссылка
        await users_db.delete_project_by_id(payload)
    else:
        text = '<b>Не могу удалить этот проект.</b>'
    await query.message.edit_text(text)


@dp.message_handler(DeepLinkPrefix(Prefixes.SEND_BID_))
async def ask_bid_text(msg: types.Message, payload: str):
    """Запрашивает текст для заявки у исполнителя или отправляет на регистрацию."""
    worker_id = msg.from_user.id
    account = await users_db.get_account_by_id(worker_id)
    profile = account.get('profile') if account else None
    project = await users_db.get_project_by_id(payload)

    if not profile:
        await msg.answer('Сначала пройдите регистрацию')
        return RegistrationConv

    if not project:
        await msg.answer('<b>Этот проект уже удален</b>')
        return

    client_id = project['client_id']
    if worker_id == client_id:
        await msg.answer('<b>Вы не можете взять свой проект</b>')
        return

    await States.ask_bid_text.set()
    await msg.answer('Отправьте текст для заявки:', reply_markup=markup.cancel_kb)
    return {'project_id': payload, 'client_id': client_id}


@dp.message_handler(state=States.ask_bid_text)
async def send_bid(msg: types.Message, state: FSMContext):
    """Отправялет заявку заказчику."""
    bid_text = msg.text

    if not 15 < len(bid_text) < 500:
        return HandleException('Ошибка, текст заявки должен быть от 15 до 500 символов')
    if bid_text.startswith('/start'):
        return HandleException('Ошибка, отправьте текст для заявки')

    bid_data = await state.get_data()
    client_id = bid_data['client_id']
    project_id = bid_data['project_id']

    bid = Bid(client_id, project_id, msg.from_user.id, bid_text)
    bid_id = await users_db.add_bid_test(bid)  # сохранение заявки
    full_bid_text = await funcs.get_worker_bid_text(msg.from_user.id, project_id, bid_text)
    keyboard = inline_funcs.for_bid(bid_id)

    await bot.send_message(client_id, full_bid_text, reply_markup=keyboard)  # отправка заказчику
    await msg.answer('Заявка отправлена', reply_markup=markup.main_kb)
    await state.finish()
