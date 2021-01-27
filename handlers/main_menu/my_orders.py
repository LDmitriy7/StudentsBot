from aiogram import types

from functions import common as cfuncs
from loader import dp, users_db


@dp.message_handler(text='Мои заказы 💼')
async def send_orders(msg: types.Message):
    projects = await users_db.get_projects_by_user(client_id=msg.from_user.id)
    if projects:
        await msg.answer('<b>Список заказов:</b>')
        await cfuncs.send_projects(msg, projects, del_button=True)
    else:
        await msg.answer('<b>У вас нет ни одного заказа</b>')
