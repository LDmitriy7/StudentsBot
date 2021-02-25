from aiogram import types

import functions as funcs
import keyboards as KB
from loader import dp, users_db


@dp.message_handler(text=KB.ForWorker.SEARCH_ORDERS)
async def find_orders(msg: types.Message, user_id):
    account = await users_db.get_account_by_id(user_id)
    if not account.subjects:
        return '<b>Вы еще не выбрали ни одного предмета</b>'

    projects = await users_db.get_projects_by_subjects(account.subjects)
    if projects:
        await msg.answer('<b>Подходящие заказы:</b>')
        await funcs.send_projects(projects, pick_btn=True)
    else:
        await msg.answer('<b>Не найдено подходящих заказов</b>')
