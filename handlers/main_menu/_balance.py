from aiogram import types
from aiogram.dispatcher import FSMContext

from functions import balance as funcs, common as cfuncs
from keyboards import markup, inline_text
from keyboards.inline_text import BalanceKeyboard
from loader import bot, dp, users_db
from states import MiscStates


@dp.pre_checkout_query_handler(state='*')
async def confirm_deposit(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT, state='*')
async def accrue_money(msg: types.Message):
    amount = int(msg.successful_payment.total_amount) // 100
    keyboard = markup.main_kb
    await users_db.incr_balance(msg.from_user.id, amount)
    await msg.answer('Баланс успешно пополнен!', reply_markup=keyboard)


@dp.message_handler(text='Баланс 🤑')
async def send_balance(msg: types.Message):
    balance = await cfuncs.get_balance(msg)
    text = f'Ваш баланс: {balance} грн'
    keyboard = inline_text.balance
    await msg.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(text=BalanceKeyboard.DEPOSIT_MONEY)
async def ask_deposit_amount(query: types.CallbackQuery):
    await MiscStates.ask_deposit_amount.set()
    keyboard = markup.cancel_kb
    await query.answer()
    await query.message.answer('Введите количество (в гривнах):', reply_markup=keyboard)


@dp.message_handler(state=MiscStates.ask_deposit_amount)
async def process_deposit(msg: types.Message, state: FSMContext):
    amount = msg.text
    if amount.isdigit() and int(amount) > 0:
        price = int(amount)
        invoice_data = funcs.make_invoice(msg, price)
        await bot.send_invoice(**invoice_data)
        await state.finish()
    else:
        await msg.answer('Ошибка, введите верное число')


@dp.callback_query_handler(text=BalanceKeyboard.WITHDRAW_MONEY)
async def ask_withdraw_amount(query: types.CallbackQuery):
    await MiscStates.ask_withdraw_amount.set()
    keyboard = markup.cancel_kb
    await query.answer()
    await query.message.answer('Введите количество (в гривнах):', reply_markup=keyboard)


@dp.message_handler(state=MiscStates.ask_withdraw_amount)
async def process_withdraw(msg: types.Message, state: FSMContext):
    amount = msg.text
    balance = await cfuncs.get_balance(msg)

    if amount.isdigit() and 0 < int(amount) < balance:
        price = -int(amount)
        await users_db.incr_balance(msg.from_user.id, price)
        await msg.answer('Заявка заполнена.', reply_markup=markup.main_kb)
        await state.finish()
    else:
        await msg.answer('Ошибка, введите верное число')