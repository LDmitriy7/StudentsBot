from aiogram import types

import functions as funcs
from loader import dp, users_db


@dp.message_handler(text='Поиск заказов')
async def find_orders(msg: types.Message):
    account = await users_db.get_account_by_id(msg.from_user.id)
    subjects = account.subjects
    if not subjects:
        await msg.answer('<b>Вы еще не выбрали ни одного предмета</b>')
        return

    projects = await users_db.get_projects_by_subjects(subjects)
    if projects:
        await msg.answer('<b>Подходящие заказы:</b>')
        await funcs.send_projects(msg.from_user.id, projects, pick_btn=True)
    else:
        await msg.answer('<b>Не найдено подходящих заказов</b>')
