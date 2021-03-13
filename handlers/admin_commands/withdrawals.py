from aiogram import types, html
from aiogram.utils.keyboards2 import InlineKeyboard, InlineButton

from config import ADMIN_IDS
from loader import dp, users_db


class WithdrawKB(InlineKeyboard):
    PAID_UP = InlineButton('Оплачено', 'withdraw:delete_from_base:')

    def __init__(self, withdrawal_id: str):
        self.PAID_UP += withdrawal_id
        super().__init__()


@dp.message_handler(commands='withdrawals', user_id=ADMIN_IDS)
async def send_all_withdrawals(msg: types.Message):
    withdrawals = await users_db.get_all_withdrawals()
    if withdrawals:
        await msg.answer(html.b('Все заявки на вывод средств:'))
        for w in withdrawals:
            text = f'Пользователь - {w.user_id}\nСумма - {w.amount} грн.'
            await msg.answer(text, WithdrawKB(w.id))
    else:
        await msg.answer('Нет ни одной заявки')


@dp.callback_query_handler(button=WithdrawKB.PAID_UP, user_id=ADMIN_IDS)
async def mark_withdrawal(msg: types.Message, suffix: str):
    updated_text = f'{html.b("[Оплачено]")}\n{msg.text}'
    await users_db.delete_withdrawal_by_id(suffix)
    await msg.edit_text(updated_text)
