"""Все для входа в создание проекта с отправкой в канал/лично/самостоятельно."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData

import functions as funcs
import keyboards as KB
import texts
from data_types import Prefixes, SendTo, TextQueries
from filters import DeepLinkPrefix
from loader import dp, users_db
from questions import CreateProjectConv, RegistrationConv


@dp.message_handler(text=KB.Main.CREATE_POST)
async def entry_create_post(msg: types.Message):
    return UpdateData({'send_to': SendTo.CHANNEL}, new_state=CreateProjectConv)


@dp.message_handler(text=KB.Main.PERSONAL_PROJECT)
async def ask_user_role(msg: types.Message):
    await msg.answer(texts.start_personal_project, reply_markup=KB.UserRoles())


@dp.callback_query_handler(text=KB.UserRoles.WORKER)
async def send_invite_project_keyboard(query: types.CallbackQuery):
    account = await users_db.get_account_by_id(query.from_user.id)
    if account and account.profile:
        text = 'Выберите <b>заказчика</b> из списка своих чатов'
        keyboard = KB.invite_project
        await query.message.edit_text(text, reply_markup=keyboard)
    else:
        await query.message.edit_text('Сначала пройдите регистрацию')
        return UpdateData(new_state=RegistrationConv)


@dp.inline_handler(text=TextQueries.INVITE_PROJECT)
async def send_project_invite_to_client(query: types.InlineQuery):
    article = await funcs.form_invite_project_article()
    await query.answer([article], cache_time=0, is_personal=True)


@dp.callback_query_handler(text=KB.UserRoles.CLIENT)
async def entry_personal_project(query: types.CallbackQuery):
    await query.message.edit_text('Сначала заполните проект')
    return UpdateData({'send_to': None}, new_state=CreateProjectConv)


@dp.message_handler(DeepLinkPrefix(Prefixes.INVITE_PROJECT_))
async def entry_personal_project_with_worker(msg: types.Message, payload: str):
    worker_id = int(payload)
    if msg.from_user.id == worker_id:
        return '<b>Вы сами не можете заполнить проект</b>'
    return UpdateData({'worker_id': worker_id, 'send_to': SendTo.WORKER}, new_state=CreateProjectConv)
