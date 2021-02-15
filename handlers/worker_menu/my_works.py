from aiogram import types

import functions as funcs
from loader import dp, users_db


@dp.message_handler(text='Мои работы')
async def send_works(msg: types.Message):
    projects = await users_db.get_projects_by_user(worker_id=msg.from_user.id)
    if projects:
        await msg.answer('<b>Список работ:</b>')
        await funcs.send_projects(projects, worker_chat_btn=True)
    else:
        await msg.answer('<b>У вас нет ни одной работы</b>')
