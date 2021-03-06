"""Все для входа в создание проекта с отправкой в канал/лично/самостоятельно."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText

import functions as funcs
import keyboards as KB
import texts
from data_types import SendTo
from loader import dp, users_db
from questions import CreateProjectConv, RegistrationConv


@dp.message_handler(text=KB.main.CREATE_POST)
async def entry_create_post():
    return UpdateData({'send_to': SendTo.CHANNEL}, new_state=CreateProjectConv)


@dp.message_handler(text=KB.main.PERSONAL_PROJECT)
async def ask_user_role():
    return QuestText(texts.start_personal_project, KB.user_roles)


@dp.callback_query_handler(text=KB.user_roles.WORKER)
async def send_invite_project_keyboard(msg: types.Message, user_id):
    account = await users_db.get_account_by_id(user_id)
    if account and account.profile:
        text = 'Выберите <b>заказчика</b> из списка своих чатов'
        await msg.edit_text(text, reply_markup=KB.choose_invite_chat)
    else:
        await msg.edit_text('Сначала пройдите регистрацию')
        return UpdateData(new_state=RegistrationConv)


@dp.inline_handler(button=KB.choose_invite_chat.INVITE_QUERY)
async def send_project_invite_to_client(iquery: types.InlineQuery):
    article = await funcs.form_invite_project_article()
    await iquery.answer([article], cache_time=0, is_personal=True)


@dp.callback_query_handler(text=KB.user_roles.CLIENT)
async def entry_personal_project(msg: types.Message):
    await msg.edit_text('Сначала заполните проект')
    return UpdateData({'send_to': None}, new_state=CreateProjectConv)


@dp.message_handler(button=KB.InviteProject.START_LINK)
async def entry_personal_project_with_worker(user_id, suffix: str):
    worker_id = int(suffix)
    if user_id == worker_id:
        return '<b>Вы сами не можете заполнить проект</b>'
    return UpdateData({'worker_id': worker_id, 'send_to': SendTo.WORKER}, new_state=CreateProjectConv)
