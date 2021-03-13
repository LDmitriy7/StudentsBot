"""Наборы всех обычных состояний бота."""
from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import ConvStatesGroup, ConvState
from aiogram.contrib.questions import QuestText
from aiogram.utils.markdown import hbold as b

import functions as funcs
import keyboards as KB
from config import MAIN_ADMIN_ID
from data_types import data_models
from loader import bot, dp, users_db


class WithdrawMoney(ConvStatesGroup):
    amount = ConvState(QuestText('Введите сумму списания', KB.back))


@dp.message_handler(text=KB.main.BALANCE)
async def send_balance():
    balance = await funcs.get_account_balance()
    return QuestText(f'Ваш баланс: {balance} грн', KB.balance)


@dp.callback_query_handler(button=KB.balance.DEPOSIT_MONEY)
async def deposit_money(msg: types.Message, user_id):
    text = f'Оплатите желаемую сумму через один из банков, обязательно укажите {user_id} в комментарии'
    await msg.answer(text, reply_markup=KB.payment)


@dp.callback_query_handler(button=KB.payment.CONFIRM)
async def confirm_payment(query: types.CallbackQuery, user_id):
    text = b(f'Запрос на проверку оплаты от пользователя {user_id}:')
    await bot.send_message(MAIN_ADMIN_ID, text, reply_markup=KB.ControlUser(user_id))
    await query.answer('Вы зачислим вам деньги, как только проверим оплату', show_alert=True)


@dp.callback_query_handler(text=KB.balance.WITHDRAW_MONEY)
async def ask_withdraw_amount():
    return UpdateData(new_state=WithdrawMoney)


@dp.message_handler(state=WithdrawMoney.amount)
async def process_withdraw(text: str, user_id: int):
    if not text.isdigit():
        return 'Ошибка, введите только число'

    amount = int(text)
    balance = await funcs.get_account_balance()

    if not (0 < amount <= balance):
        return 'Ошибка, недопустимая сумма'

    await users_db.incr_balance(user_id, -amount)
    await users_db.add_withdrawal(data_models.Withdrawal(user_id, amount))
    return UpdateData(), QuestText('Ваша заявка будет рассмотрена в течение ...', KB.main)
