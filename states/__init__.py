# from states.main import *

from aiogram.dispatcher.filters.state import State, StatesGroup


class MiscStates(StatesGroup):
    ask_bid_text = State()
