"""Наборы всех обычных состояний бота."""
from aiogram.dispatcher.filters.state import State, StatesGroup


class MiscStates(StatesGroup):
    ask_bid_text = State()
    change_subjects = State()


class Payment(StatesGroup):
    ask_deposit_amount = State()
    ask_withdraw_amount = State()
    ask_work_price = State()


class ChangeProfile(StatesGroup):
    nickname = State()
    phone_number = State()
    email = State()
    biography = State()
    works = State()
