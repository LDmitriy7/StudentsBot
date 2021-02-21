from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardButton as IButton
from aiogram.utils.helper import Helper, Item
from dataclasses import dataclass


@dataclass
class ResizedKeyboard(ReplyKeyboardMarkup, Helper):
    """ReplyKeyboardMarkup with [resize_keyboard=True, row_width=2]"""
    row_width: int = 2

    def __contains__(self, item) -> bool:
        buttons = []
        for row in self.keyboard:
            buttons.extend(row)
        return item in buttons

    def buttons(self) -> list[str]:
        result = []
        for name, value in vars(self).items():
            if name.isupper() and value:
                result.append(value)
        return result

    def __post_init__(self):
        super().__init__(resize_keyboard=True, row_width=self.row_width)
        for item in self.buttons():
            self.insert(item)


class InlineButton(Item):
    def __init__(self, text: str):
        self.text = text
        super().__init__()


class InlineKeyboard(InlineKeyboardMarkup, Helper):

    def data_row(self, text: str, callback_data: str):
        self.row(InlineKeyboardButton(text, callback_data=callback_data))

    def url_row(self, text: str, url: str):
        self.row(InlineKeyboardButton(text, url=url))

    def __post_init__(self):
        super().__init__()
        for item in self.all():
            if self.__dict__[item]:
                self.data_row(self.__class__.__dict__[item].text, item)


class SameInlineKeyboard(InlineKeyboardMarkup):
    BUTTONS = []

    def __init__(self, row_width: int = 2):
        super().__init__(row_width)
        self.add(*get_same_inline_button(self.BUTTONS))


def make_keyboard(*rows: dict[str, bool]) -> ResizedKeyboard:
    kb = ResizedKeyboard()
    for row in rows:
        kb.row(*[button for button, boolean in row.items() if boolean])
    return kb


def get_same_inline_button(buttons: list[str]):
    """Создает инлайн-кнопки из обычных, где [callback_data = text]"""
    return [IButton(btn, callback_data=btn) for btn in buttons]
