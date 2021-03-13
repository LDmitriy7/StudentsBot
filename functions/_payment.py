"""Contain funcs for work with payments and balance."""

from aiogram.dispatcher.currents import CurrentObjects

from loader import users_db

__all__ = ['get_account_balance']


@CurrentObjects.decorate
async def get_account_balance(*, user_id) -> int:
    """Return balance of account or 0."""
    account = await users_db.get_account_by_id(user_id)
    balance = account.balance if account else 0
    return balance or 0
