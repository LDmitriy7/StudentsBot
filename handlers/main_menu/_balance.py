"""Наборы всех обычных состояний бота."""
from aiogram import types
from aiogram.contrib.questions import QuestText
from aiogram.utils.markdown import hbold as b
from aiogram.utils.keyboards2 import ReplyKeyboard

import functions as funcs
import keyboards as KB
from config import MAIN_ADMIN_ID
from loader import bot, dp


class ConfirmPaymentKB(ReplyKeyboard):
    CONFIRM = 'Подтвердить оплату'


@dp.message_handler(text=KB.main.BALANCE)
async def send_balance():
    balance = await funcs.get_account_balance()
    return QuestText(f'Ваш баланс: {balance} грн', KB.balance)


@dp.callback_query_handler(button=KB.balance.DEPOSIT_MONEY)
async def deposit_money(msg: types.Message, user_id):
    text1 = f'Оплатите желаемую сумму через один из банков, обязательно укажите {user_id} в комментарии'
    text2 = 'Пояснение ...'
    await msg.answer(text1, reply_markup=KB.payment)
    return QuestText(text2, ConfirmPaymentKB())


@dp.message_handler(button=ConfirmPaymentKB.CONFIRM)
async def confirm_payment(user_id):
    text = b(f'Запрос на проверку оплаты от пользователя {user_id}:')
    await bot.send_message(MAIN_ADMIN_ID, text, reply_markup=KB.ControlUser(user_id))
    return QuestText('Вы зачислим вам деньги, как только проверим оплату', KB.main)

# @dp.callback_query_handler(text=BalanceKeyboard.WITHDRAW_MONEY)
# async def ask_withdraw_amount(query: types.CallbackQuery):
#     await States.ask_withdraw_amount.set()
#     return QuestText('Введите количество (в гривнах):', BackKeyboard(BACK=None))
#
#
# @dp.message_handler(state=States.ask_withdraw_amount)
# async def process_withdraw(msg: types.Message, state: FSMContext):
#     amount = msg.text
#     balance = await funcs.get_account_balance()
#
#     if amount.isdigit() and 0 < int(amount) < balance:
#         price = -int(amount)
#         await users_db.incr_balance(msg.from_user.id, price)
#         await msg.answer('Заявка заполнена.', reply_markup=MainKeyboard())
#         await state.finish()
#     else:
#         await msg.answer('Ошибка, введите верное число')
#
