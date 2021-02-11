from aiogram import types

from config import PAYMENTS_PROVIDER_TOKEN

__all__ = ['make_invoice', 'get_account_balance']

from loader import users_db


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


async def get_account_balance(user_id: int) -> int:
    """Return balance of account or 0."""
    account = await users_db.get_account_by_id(user_id)
    balance = account.balance if account else 0
    return balance
