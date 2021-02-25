from aiogram.types import ForceReply as _ForceReply
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton as IButton
from aiogram.types.base import MetaTelegramObject
from aiogram.utils.helper import Helper, Item


class InstantKeyboard(MetaTelegramObject):
    """Create Keyboard instance instead of class (If class.instant == True)."""

    def __new__(mcs, cls_name, bases, namespace: dict):
        cls = super().__new__(mcs, cls_name, bases, namespace)

        for base in bases:
            if base in [ReplyKeyboardMarkup, InlineKeyboardMarkup]:
                return cls

        if getattr(cls, 'instant', None) is True:
            return cls()
        return cls


class InlineInstantKeyboard(InstantKeyboard):

    def __new__(mcs, cls_name, bases, namespace: dict):
        inline_buttons = []

        for name, prop in namespace.items():
            if name.isupper() and prop:
                inline_buttons.append(IButton(prop, callback_data=name))
                namespace[name] = name

        namespace['inline_buttons'] = inline_buttons
        cls = super().__new__(mcs, cls_name, bases, namespace)
        return cls


class InlineKeyboard(InlineKeyboardMarkup, metaclass=InlineInstantKeyboard):
    instant = True
    rows_width = []
    default_width = 2

    def __init__(self):
        super().__init__(row_width=self.default_width)

        buttons = self.inline_buttons
        for rw in self.rows_width:
            row, buttons = buttons[:rw], buttons[rw:]
            self.row(*row)

        if buttons:
            self.add(*buttons)


class ReplyKeyboard(ReplyKeyboardMarkup, metaclass=InstantKeyboard):
    """Upgraded ReplyKeyboardMarkup for inheritance.
    Sublasses will be created as instances if cls.instant == True.
    You can specify buttons as constants (uppercase only) or explicitly:

    class MyKeyboard(ReplyKeyboard):
        START = 'Hello'
        END = 'bye'

    class MyKeyboard2(ReplyKeyboard):
        buttons = ['text1', 'text2', 'text3']
    """

    instant = True
    rows_width = []
    default_width = 2

    def __init__(self):
        super().__init__(resize_keyboard=True, row_width=self.default_width)

        buttons = self.buttons
        for rw in self.rows_width:
            row, buttons = buttons[:rw], buttons[rw:]
            self.row(*row)

        if buttons:
            self.add(*buttons)

    def __contains__(self, item) -> bool:
        return item in self.buttons

    @classmethod
    @property
    def buttons(cls) -> list[str]:
        result = []
        for name, value in vars(cls).items():
            if name.isupper() and value:
                result.append(value)
        return result


ForceReply = _ForceReply()


class InlineButton(Item):
    def __init__(self, text: str):
        self.text = text
        super().__init__()


# class InlineKeyboard(InlineKeyboardMarkup, Helper):
#
#     def data_row(self, text: str, callback_data: str):
#         self.row(IButton(text, callback_data=callback_data))
#
#     def url_row(self, text: str, url: str):
#         self.row(IButton(text, url=url))
#
#     def __post_init__(self):
#         super().__init__()
#         for item in self.all():
#             if self.__dict__[item]:
#                 self.data_row(self.__class__.__dict__[item].text, item)
#

class SameInlineKeyboard(InlineKeyboardMarkup, metaclass=InstantKeyboard):
    buttons = []
    instant = True
    rows_width = []
    default_width = 2

    def __init__(self):
        super().__init__(row_width=self.default_width)

        buttons = get_same_inline_button(self.buttons)
        for rw in self.rows_width:
            row, buttons = buttons[:rw], buttons[rw:]
            self.row(*row)

        if buttons:
            self.add(*buttons)


def make_keyboard(*rows: dict[str, bool]) -> ReplyKeyboard:
    kb = ReplyKeyboard()
    for row in rows:
        kb.row(*[button for button, boolean in row.items() if boolean])
    return kb


def get_same_inline_button(buttons: list[str]):
    """Создает инлайн-кнопки из обычных, где [callback_data = text]"""
    return [IButton(btn, callback_data=btn) for btn in buttons]
