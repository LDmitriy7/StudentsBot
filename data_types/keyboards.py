from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.helper import Helper


class ResizedKeyboardMarkup(ReplyKeyboardMarkup):
    """ReplyKeyboardMarkup with [resize_keyboard=True, row_width=2]"""

    def __init__(self, row_width: int = 2):
        super().__init__(resize_keyboard=True, row_width=row_width)

    def __repr__(self):
        return super().__str__()

    def __contains__(self, item):
        buttons = []
        for row in self.keyboard:
            buttons.extend(row)
        return item in buttons


class InlineKeyboard(InlineKeyboardMarkup, Helper):
    def data_row(self, text: str, callback_data: str):
        self.row(InlineKeyboardButton(text, callback_data=callback_data))

    def url_row(self, text: str, url: str):
        self.row(InlineKeyboardButton(text, url=url))


def make_keyboard(*rows: dict[str, bool]) -> ResizedKeyboardMarkup:
    kb = ResizedKeyboardMarkup()
    for row in rows:
        kb.row(*[button for button, boolean in row.items() if boolean])
    return kb
