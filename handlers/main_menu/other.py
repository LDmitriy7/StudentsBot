"""Кнопки 'Предложить идею', 'Инструкция' и 'Меню исполнителя'."""
from aiogram import types

from keyboards import markup
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
    profile = account.get('profile') if account else None
    if profile:
        await msg.answer('Меню исполнителя:', reply_markup=markup.worker_kb)
    else:
        await msg.answer('Сначала пройдите регистрацию')
        return RegistrationConv
