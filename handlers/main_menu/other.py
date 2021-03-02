"""Кнопки 'Предложить идею', 'Инструкция' и 'Меню исполнителя'."""
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText

import keyboards as KB
import texts
from loader import dp, users_db
from questions.registration import RegistrationConv


@dp.message_handler(text=KB.main.OFFER_IDEA)
async def suggest_idea():
    return texts.suggest_idea


@dp.message_handler(text=KB.main.GUIDE)
async def send_guide():
    return texts.guide


@dp.message_handler(text=KB.main.WORKER_MENU)
async def worker_menu(user_id: int):
    account = await users_db.get_account_by_id(user_id)
    if account and account.profile:
        return QuestText('Меню исполнителя:', KB.for_worker)
    else:
        return UpdateData(new_state=RegistrationConv), 'Сначала пройдите регистрацию'
