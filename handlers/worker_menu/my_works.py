from loader import dp, users_db
from aiogram import types
from functions import common as cfuncs


@dp.message_handler(text='Мои работы')
async def send_works(msg: types.Message):
    projects = await users_db.get_projects_by_user(worker_id=msg.from_user.id)
    if projects:
        await msg.answer('<b>Список работ:</b>')
        await cfuncs.send_projects(msg, projects, with_note=False)
    else:
        await msg.answer('<b>У вас нет ни одной работы</b>')
