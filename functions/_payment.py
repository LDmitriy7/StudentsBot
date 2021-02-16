"""Contain funcs for work with payments and balance."""
from aiogram import types

from config import PAYMENTS_PROVIDER_TOKEN
from loader import users_db

__all__ = ['make_invoice', 'get_account_balance']


# deprecated
def make_invoice(chat_id: int, price: int) -> dict:
    """Создает данные для отправки платежки."""
    prices = [types.LabeledPrice('Пополнение баланса', price * 100)]

    invoice_data = dict(
        chat_id=chat_id,
        title='Пополнение',
        description='Пополнение баланса',
        provider_token=PAYMENTS_PROVIDER_TOKEN,
        currency='uah',
        prices=prices,
        payload='test',
        start_parameter='test2',
    )
    return invoice_data


async def get_account_balance(user_id: int = None) -> int:
    """Return balance of account or 0.
    By default: user = current User
    """
    if user_id is None:
        user_id = types.User.get_current().id

    account = await users_db.get_account_by_id(user_id)
    balance = account.balance if account else 0
    return balance or 0
