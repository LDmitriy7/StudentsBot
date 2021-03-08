"""TODO: Change docs."""
from typing import Union, TypeVar, Optional

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import InlineKeyboardButton, KeyboardButton

from loader import dp

T = TypeVar('T')


def to_iterable(obj):
    if not isinstance(obj, (list, tuple, set, frozenset)):
        obj = [obj]
    return obj


class CallbackQueryButton(BoundFilter):
    """Check if callback query data startswith button.callback_data, return suffix.
    Takes inline button with callback_data or already str."""

    key = 'button'
    Button = Union[str, InlineKeyboardButton]

    def __init__(self, button: Union[Button, list[Button]]):
        self.buttons_data = []

        for item in to_iterable(button):
            if isinstance(item, str):
                button_data = item
            else:
                button_data = item.callback_data

            assert isinstance(button_data, str), f'Invalid button for {self.__class__.__name__} filter'
            self.buttons_data.append(button_data)

    @staticmethod
    def check_one(query: types.CallbackQuery, button_data: str) -> Optional[dict]:
        if query.data.startswith(button_data):
            return {'suffix': query.data.removeprefix(button_data) or None}

    async def check(self, query: types.CallbackQuery) -> Union[dict, bool]:
        for button_data in self.buttons_data:
            result = self.check_one(query, button_data)
            if result:
                return result
        return False


class InlineQueryButton(BoundFilter):
    """Check if inline query data startswith button.switch_inline_query[_current_chat], return suffix.
    Takes inline button with switch_inline_query[_current_chat] or already str."""

    key = 'button'
    Button = Union[str, InlineKeyboardButton]

    def __init__(self, button: Union[Button, list[Button]]):
        self.buttons_data = []

        for item in to_iterable(button):
            if isinstance(item, str):
                button_data = item
            elif item.switch_inline_query is not None:
                button_data = item.switch_inline_query
            else:
                button_data = item.switch_inline_query_current_chat

            assert isinstance(button_data, str), f'Invalid button for {self.__class__.__name__} filter'
            self.buttons_data.append(button_data)

    @staticmethod
    def check_one(query: types.InlineQuery, button_data: str) -> Optional[dict]:
        if query.query.startswith(button_data):
            return {'suffix': query.query.removeprefix(button_data) or None}

    async def check(self, query: types.InlineQuery) -> Union[dict, bool]:
        for button_data in self.buttons_data:
            result = self.check_one(query, button_data)
            if result:
                return result
        return False


class MessageButton(BoundFilter):
    """Check if message text (or start's command param) startswith button.text (or url's start param),
    return suffix.
    Takes keyboard button, inline button with url (deeplink) or already str."""

    key = 'button'
    Button = Union[str, KeyboardButton, InlineKeyboardButton]

    def __init__(self, button: Union[Button, list[Button]]):
        self.buttons_data = []

        for item in to_iterable(button):
            if isinstance(item, str):
                button_data = item
            elif isinstance(item, KeyboardButton):
                button_data = item.text
            elif isinstance(item, InlineKeyboardButton):
                assert '?start=' in item.url, f'Button.url for {self.__class__.__name__} filter must be deeplink.'
                deeplink = item.url.split('?start=')[-1]
                button_data = f'/start {deeplink}'
            else:
                raise TypeError(f'Invalid button for {self.__class__.__name__} filter.')

            self.buttons_data.append(button_data)

    @staticmethod
    def check_one(msg: types.Message, button_data: str) -> Optional[dict]:
        if msg.text.startswith(button_data):
            return {'suffix': msg.text.removeprefix(button_data) or None}

    async def check(self, msg: types.Message) -> Union[dict, bool]:
        for button_data in self.buttons_data:
            result = self.check_one(msg, button_data)
            if result:
                return result
        return False


dp.bind_filter(CallbackQueryButton, event_handlers=[dp.callback_query_handlers])
dp.bind_filter(InlineQueryButton, event_handlers=[dp.inline_query_handlers])
dp.bind_filter(MessageButton, event_handlers=[dp.message_handlers])


class CallbackQueryButtonStrict:
    raise NotImplementedError


class InlineQueryButtonStrict:
    raise NotImplementedError


class MessageButtonStrict:
    raise NotImplementedError

# -------------
# btn1 = InlineKeyboardButton('test', switch_inline_query='test')
# btn2 = InlineKeyboardButton('test', switch_inline_query_current_chat='test')
# btn3 = InlineKeyboardButton('test', callback_data='test')
# btn4 = InlineKeyboardButton('test', url='test')
# btn5 = InlineKeyboardButton('122', url='https://t.me/bot?start=send:bid:')
# btn6 = 'test'
#
# query1 = types.CallbackQuery(data='error')
# query2 = types.CallbackQuery(data='test:34342')
#
# iquery1 = types.InlineQuery(query='test:3434')
# iquery2 = types.InlineQuery(query='error')
#
# msg1 = types.Message(text='/start send:bid:4324')
# msg2 = types.Message(text='test')
#
# _filter = CallbackQueryButton(btn3)
# _filter = MessageButton(['1234', InlineKeyboardButton('122', url='https://t.me/bot?start=send:bid:')])
# _filter = MessageButton(btn6)
# _filter = ButtonPrefixMessage(['test:', 'error'])
# coro = _filter.check(msg2)  # error
# coro = _filter.check(msg2)
# coro = _filter.check(msg2)
#
# from asyncio import run
#
# print(run(coro))
