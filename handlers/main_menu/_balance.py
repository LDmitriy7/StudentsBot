"""Наборы всех обычных состояний бота."""
from aiogram import types
from aiogram.contrib.questions import QuestText
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hbold as b

import functions as funcs
import keyboards as KB
from config import MAIN_ADMIN_ID
from loader import bot, dp


@dp.message_handler(text=KB.main.BALANCE)
async def send_balance():
    balance = await funcs.get_account_balance()
    return QuestText(f'Ваш баланс: {balance} грн', KB.balance)


@dp.callback_query_handler(text=KB.balance.DEPOSIT_MONEY)
async def deposit_money(user_id):
    text = f'Оплатите желаемую сумму через один из банков, обязательно укажите {user_id} в комментарии'
    return QuestText(text, KB.payment)


@dp.callback_query_handler(text=KB.payment.ASK_CONFIRM)
async def confirm_payment(query: types.CallbackQuery, user_id):
    await bot.send_message(MAIN_ADMIN_ID, b(f'Пользователь {user_id} запросил проверку оплаты'))
    await query.answer('Вы зачислим вам деньги, как только проверим оплату', show_alert=True)

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
