from aiogram import types
from aiogram.contrib.questions import QuestText
from aiogram.dispatcher import FSMContext

import functions as funcs
from data_types.states import Payment as States
from keyboards.inline_plain import BalanceKeyboard
from keyboards.markup import MainKeyboard, BackKeyboard
from loader import bot, dp, users_db


@dp.pre_checkout_query_handler(state='*')
async def confirm_deposit(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT, state='*')
async def accrue_money(msg: types.Message):
    amount = int(msg.successful_payment.total_amount) // 100
    keyboard = MainKeyboard()
    await users_db.incr_balance(msg.from_user.id, amount)
    await msg.answer('Баланс успешно пополнен!', reply_markup=keyboard)


@dp.message_handler(text=MainKeyboard.BALANCE)
async def send_balance(msg: types.Message):
    balance = await funcs.get_account_balance()
    text = f'Ваш баланс: {balance} грн'
    keyboard = BalanceKeyboard()
    await msg.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(text=BalanceKeyboard.DEPOSIT_MONEY)
async def ask_deposit_amount(query: types.CallbackQuery):
    await States.ask_deposit_amount.set()
    return QuestText('Введите количество (в гривнах):', BackKeyboard(BACK=None))


@dp.message_handler(state=States.ask_deposit_amount)
async def process_deposit(msg: types.Message, state: FSMContext):
    amount = msg.text
    if amount.isdigit() and int(amount) > 0:
        price = int(amount)
        invoice_data = funcs.make_invoice(msg.chat.id, price)
        await bot.send_invoice(**invoice_data)
        await state.finish()
    else:
        await msg.answer('Ошибка, введите верное число')


@dp.callback_query_handler(text=BalanceKeyboard.WITHDRAW_MONEY)
async def ask_withdraw_amount(query: types.CallbackQuery):
    await States.ask_withdraw_amount.set()
    return QuestText('Введите количество (в гривнах):', BackKeyboard(BACK=None))


@dp.message_handler(state=States.ask_withdraw_amount)
async def process_withdraw(msg: types.Message, state: FSMContext):
    amount = msg.text
    balance = await funcs.get_account_balance()

    if amount.isdigit() and 0 < int(amount) < balance:
        price = -int(amount)
        await users_db.incr_balance(msg.from_user.id, price)
        await msg.answer('Заявка заполнена.', reply_markup=MainKeyboard())
        await state.finish()
    else:
        await msg.answer('Ошибка, введите верное число')
