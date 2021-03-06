from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import SingleConvStatesGroup, ConvState, QuestText

import functions as funcs
import keyboards as KB
import texts
from config import ADMIN_IDS
from data_types import ProjectStatuses
from loader import dp, users_db


class AdminStates(SingleConvStatesGroup):
    ask_user_for_balance = ConvState(QuestText('Введите ID пользователя', KB.back))


@dp.message_handler(commands='balance', user_id=ADMIN_IDS)
async def ask_user_for_balance():
    return UpdateData(new_state=AdminStates.ask_user_for_balance)


@dp.message_handler(state=AdminStates.ask_user_for_balance, user_id=ADMIN_IDS)
async def send_balance(text: str):
    if not text.isdigit():
        return 'Ошибка, введите ID (число)'
    balance = await funcs.get_account_balance(user_id=int(text))
    return UpdateData(), QuestText(f'Баланс пользователя: {balance} грн.', KB.main)


@dp.message_handler(commands='admin', user_id=ADMIN_IDS)
async def send_admin_commands():
    return texts.admin_commands


@dp.message_handler(commands='allMoney', user_id=ADMIN_IDS)
async def send_all_money_amount():
    account = await users_db.get_all_accounts()
    projects = await users_db.get_all_projects()

    on_balances = sum(a.balance or 0 for a in account)
    in_projects = sum(p.data.price for p in projects if p.status == ProjectStatuses.IN_PROGRESS)

    total_money = on_balances + in_projects
    return f'Всего в сервисе задействовано: {total_money} грн'
