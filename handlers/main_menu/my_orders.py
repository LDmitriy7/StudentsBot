from aiogram import types

import functions as funcs
import keyboards as KB
from loader import dp, users_db


@dp.message_handler(text=KB.Main.MY_ORDERS)
async def send_orders(msg: types.Message):
    projects = await users_db.get_projects_by_user(client_id=msg.from_user.id)
    if projects:
        await msg.answer('<b>Список заказов:</b>')
        await funcs.send_projects(projects, with_note=True, del_btn=True, client_chat_btn=True)
    else:
        await msg.answer('<b>У вас нет ни одного заказа</b>')
