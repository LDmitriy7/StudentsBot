from loader import users_db, dp
from aiogram import types
from functions import common as cfuncs


@dp.message_handler(text='Поиск заказов')
async def find_orders(msg: types.Message):
    account = await users_db.get_account_by_id(msg.from_user.id)
    subjects = account.get('subjects') if account else None
    if not subjects:
        await msg.answer('<b>Вы еще не выбрали ни одного предмета</b>')
        return

    projects = await users_db.get_projects_by_subjects(subjects)
    if projects:
        await msg.answer('<b>Подходящие заказы:</b>')
        await cfuncs.send_projects(msg, projects, with_note=False, pick_button=True)
    else:
        await msg.answer('<b>Не найдено подходящих заказов</b>')
