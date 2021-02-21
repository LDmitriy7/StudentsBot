"""Кнопки 'Предложить идею', 'Инструкция' и 'Меню исполнителя'."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData

from keyboards.markup import WorkerKeyboard
from loader import dp, users_db
from questions.registration import RegistrationConv
from texts import main as texts


@dp.message_handler(text='Предложить идею ✍')
async def suggest_idea(msg: types.Message):
    await msg.answer(texts.suggest_idea)


@dp.message_handler(text='Инструкция 📑')
async def send_guide(msg: types.Message):
    await msg.answer(texts.guide)


@dp.message_handler(text='Меню исполнителя')
async def worker_menu(msg: types.Message):
    account = await users_db.get_account_by_id(msg.from_user.id)
    if account and account.profile:
        await msg.answer('Меню исполнителя:', reply_markup=WorkerKeyboard())
    else:
        await msg.answer('Сначала пройдите регистрацию')
        return UpdateData(new_state=RegistrationConv)
