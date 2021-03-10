from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import ConvState, ConvStatesGroup, QuestText
from aiogram.utils.exceptions import TelegramAPIError

import functions as funcs
import keyboards as KB
from config import ADMIN_IDS
from loader import dp, users_db, bot
from texts import templates


class PaymentConv(ConvStatesGroup):
    ask_amount = ConvState(QuestText('Введите сумму пополнения', KB.back))


class WithdrawConv(ConvStatesGroup):
    ask_amount = ConvState(QuestText('Введите сумму снятия', KB.back))


@dp.message_handler(is_forwarded=True, user_id=ADMIN_IDS)
async def reply_on_forwarded(msg: types.Message):
    target_user = msg.forward_from.id
    print(target_user)
    text = f'Это сообщение принадлежит пользователю {target_user}'
    keyboard = KB.ControlUser(target_user)
    await msg.reply(text, reply_markup=keyboard)


@dp.callback_query_handler(button=KB.ControlUser.WATCH_BALANCE, user_id=ADMIN_IDS)
async def send_user_balance(suffix: str):
    balance = await funcs.get_account_balance(user_id=int(suffix))
    return f'Баланс этого пользователя: {balance} грн.'


@dp.callback_query_handler(button=KB.ControlUser.WATCH_PROFILE, user_id=ADMIN_IDS)
async def send_user_profile(suffix: str):
    target_user = int(suffix)
    account = await users_db.get_account_by_id(target_user)

    if not (account and account.profile):
        return 'Этот пользователь не зарегестрировал профиль'

    return templates.form_profile_template(
        account.profile.nickname,
        account.profile.phone_number or 'Не указан',
        account.profile.email or 'Не указан',
        account.page_url,
    )


@dp.callback_query_handler(button=KB.ControlUser.PAY, user_id=ADMIN_IDS)
async def ask_pay_for_user_amount(suffix: str):
    return UpdateData({'user_id': int(suffix)}, new_state=PaymentConv)


@dp.message_handler(state=PaymentConv.ask_amount, user_id=ADMIN_IDS)
async def pay_for_user(text: str, sdata: dict):
    if not text.isdigit():
        return 'Ошибка, введите число'

    amount = int(text)
    await users_db.incr_balance(sdata['user_id'], amount)

    try:
        await bot.send_message(sdata['user_id'], f'Вам начислено {amount} гривен')
    except TelegramAPIError:
        pass

    return UpdateData(), QuestText('Деньги успешно отправлены', KB.main)


@dp.callback_query_handler(button=KB.ControlUser.WITHDRAW, user_id=ADMIN_IDS)
async def ask_withdraw_amount(suffix: str):
    return UpdateData({'user_id': int(suffix)}, new_state=WithdrawConv)


@dp.message_handler(state=WithdrawConv.ask_amount, user_id=ADMIN_IDS)
async def pay_for_user(text: str, sdata: dict):
    if not text.isdigit():
        return 'Ошибка, введите число'

    amount = int(text)
    await users_db.incr_balance(sdata['user_id'], -amount)

    try:
        await bot.send_message(sdata['user_id'], f'C вашего аккаунта списано {amount} гривен')
    except TelegramAPIError:
        pass

    return UpdateData(), QuestText('Деньги успешно списаны', KB.main)
