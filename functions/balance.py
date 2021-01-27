from config import PAYMENTS_PROVIDER_TOKEN
from aiogram import types
from loader import users_db


def make_invoice(msg: types.Message, price: int) -> dict:
    prices = [types.LabeledPrice('Пополнение баланса', price * 100)]

    invoice_data = dict(
        chat_id=msg.from_user.id,
        title='Пополнение',
        description='Пополнение баланса',
        provider_token=PAYMENTS_PROVIDER_TOKEN,
        currency='uah',
        prices=prices,
        payload='test',
        start_parameter='test2',
    )
    return invoice_data


