from aiogram.dispatcher.filters.state import State, StatesGroup


class MiscStates(StatesGroup):
    ask_bid_text = State()
    ask_deposit_amount = State()
    ask_withdraw_amount = State()
    change_subjects = State()


class Projects(StatesGroup):
    ask_bid_text = State()