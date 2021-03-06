from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import ConvStatesGroup, ConvState, QuestText
from aiogram.utils.exceptions import TelegramAPIError
from aiogram.utils.keyboards import InlineKeyboard, Buttons

import keyboards as KB
from config import ADMIN_IDS
from loader import dp, users_db, bot


class ConfirmPayment(InlineKeyboard):
    CONFIRM = 'Подтвердить'
    REFUSE = Buttons.callback('Отменить', KB.DEL_MESSAGE)


keyboard = ConfirmPayment()


class PaymentConv(ConvStatesGroup):
    ask_amount = ConvState(QuestText('Введите сумму пополнения', KB.back))
    ask_user_id = ConvState(QuestText('Введите ID пользователя', KB.back_cancel))
    ask_confirm = ConvState(QuestText('Подтвердите пополнение', keyboard))


@dp.message_handler(commands=['pay'], user_id=ADMIN_IDS)
async def ask_amount():
    return UpdateData(new_state=PaymentConv)


@dp.message_handler(user_id=ADMIN_IDS, state=PaymentConv.ask_amount)
async def process_amount(text: str):
    if text.isdigit():
        return UpdateData({'amount': int(text)})
    return 'Ошибка, введите число'


@dp.message_handler(user_id=ADMIN_IDS, state=PaymentConv.ask_user_id)
async def process_user_id(text: str):
    if text.isdigit():
        return UpdateData({'user_id': int(text)})
    return 'Ошибка, введите верный ID (число)'


@dp.callback_query_handler(user_id=ADMIN_IDS, text=keyboard.CONFIRM, state=PaymentConv.ask_confirm)
async def send_money(sdata: dict):
    await users_db.incr_balance(sdata['user_id'], sdata['amount'])
    try:
        await bot.send_message(sdata['user_id'], f'Вам начислено {sdata["amount"]} гривен')
    except TelegramAPIError:
        pass
    return UpdateData(), QuestText('Деньги успешно отправлены', KB.main)
