"""Все для входа в создание проекта с отправкой в канал/лично/самостоятельно."""
from aiogram import types

from datatypes import Prefixes, SendTo, HandleException
from filters import DeepLinkPrefix
from keyboards import inline_plain, markup
from loader import dp, users_db
from questions import CreateProjectConv, RegistrationConv
from texts import main as texts


@dp.message_handler(text='Создать пост ➕')
async def entry_create_post(msg: types.Message):
    return CreateProjectConv, {'send_to': SendTo.CHANNEL}


@dp.message_handler(text='Личный проект 🤝')
async def ask_user_role(msg: types.Message):
    await msg.answer(texts.start_personal_project, reply_markup=markup.personal_project)


@dp.message_handler(text='Я исполнитель')
async def send_invite_project_keyboard(msg: types.Message):
    account = await users_db.get_account_by_id(msg.from_user.id)
    if account and account.profile:
        text = 'Выберите <b>заказчика</b> из списка своих чатов'
        keyboard = inline_plain.invite_project
        await msg.answer(text, reply_markup=keyboard)
    else:
        await msg.answer('Сначала пройдите регистрацию')
        return RegistrationConv


@dp.message_handler(text='Я заказчик')
async def entry_personal_project(msg: types.Message):
    await msg.answer('Сначала заполните проект')
    return CreateProjectConv, {'send_to': None}


@dp.message_handler(DeepLinkPrefix(Prefixes.INVITE_PROJECT_))
async def entry_personal_project_with_worker(msg: types.Message, payload: str):
    worker_id = int(payload)
    if msg.from_user.id == worker_id:
        return HandleException('<b>Вы сами не можете заполнить проект</b>')
    return CreateProjectConv, {'worker_id': worker_id, 'send_to': SendTo.WORKER}
