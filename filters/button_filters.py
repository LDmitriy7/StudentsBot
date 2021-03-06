"""TODO: Change docs."""
from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import InlineKeyboardButton, KeyboardButton

from loader import dp


class CallbackQueryButton(BoundFilter):
    """Check if callback query data equal button.callback_data.
    Takes inline button with callback_data or already str."""

    key = 'button'
    Button = Union[str, InlineKeyboardButton]

    def __init__(self, button: Union[Button, list[Button]]):
        buttons_data = []
        if not isinstance(button, (list, tuple, set)):
            button = [button]

        for item in button:
            if isinstance(item, str):
                button_data = item
            else:
                button_data = item.callback_data

            assert isinstance(button_data, str), f'Invalid data for {self.__class__.__name__} filter'
            buttons_data.append(button_data)

        self.buttons_data = buttons_data

    async def check(self, query: types.CallbackQuery) -> bool:
        return any(button_data == query.data for button_data in self.buttons_data)


class InlineQueryButton(BoundFilter):
    """Check if inline query data equal button.switch_inline_query[_current_chat].
    Takes inline button with switch_inline_query[_current_chat] or already str."""

    key = 'button'
    Button = Union[str, InlineKeyboardButton]

    def __init__(self, button: Union[Button, list[Button]]):
        buttons_data = []
        if not isinstance(button, (list, tuple, set)):
            button = [button]

        for item in button:
            if isinstance(item, str):
                button_data = item
            elif item.switch_inline_query is not None:
                button_data = item.switch_inline_query
            else:
                button_data = item.switch_inline_query_current_chat

            assert isinstance(button_data, str), f'Invalid data for {self.__class__.__name__} filter'
            buttons_data.append(button_data)

        self.buttons_data = buttons_data

    async def check(self, query: types.InlineQuery) -> bool:
        return any(button_data == query.query for button_data in self.buttons_data)


class MessageButton(BoundFilter):
    """Check if message text (or start command param) equal button.text (or url start param).
    Takes keyboard button, inline button with url (deeplink) or already str."""

    key = 'button'
    Button = Union[str, KeyboardButton, InlineKeyboardButton]

    def __init__(self, button: Union[Button, list[Button]]):
        buttons_data = []
        if not isinstance(button, (list, tuple, set)):
            button = [button]

        for item in button:
            if isinstance(item, str):
                button_data = item
            elif isinstance(item, KeyboardButton):
                button_data = item.text
            elif isinstance(item, InlineKeyboardButton):
                assert '?start=' in item.url, f'Button.url for {self.__class__.__name__} filter must be deeplink.'
                deeplink = item.url.split('?start=')[-1]
                button_data = f'/start {deeplink}'
            else:
                raise TypeError(f'Invalid button type for {self.__class__.__name__} filter.')

            buttons_data.append(button_data)

        self.buttons_data = buttons_data

    async def check(self, msg: types.Message) -> bool:
        return any(button_data == msg.text for button_data in self.buttons_data)


class CallbackQueryPrefixButton(CallbackQueryButton):
    key = 'prefix_button'
    Button = Union[str, InlineKeyboardButton]

    def __init__(self, prefix_button: Union[Button, list[Button]]):
        super().__init__(prefix_button)

    async def check(self, query: types.CallbackQuery) -> Union[dict, bool]:
        for button_data in self.buttons_data:
            if query.data.startswith(button_data):
                payload = query.data.removeprefix(button_data)
                return {'payload': payload}
        return False


class InlineQueryPrefixButton(InlineQueryButton):
    """Check if inline query data equal button.switch_inline_query[_current_chat].
    Takes inline button with switch_inline_query[_current_chat] or already str."""

    key = 'prefix_button'
    Button = Union[str, InlineKeyboardButton]

    def __init__(self, prefix_button: Union[Button, list[Button]]):
        super().__init__(prefix_button)

    async def check(self, query: types.InlineQuery) -> Union[dict, bool]:
        for button_data in self.buttons_data:
            if query.query.startswith(button_data):
                payload = query.query.removeprefix(button_data)
                return {'payload': payload}
        return False


class MessagePrefixButton(MessageButton):
    """Check if message text (or start command param) equal button.text (or url start param).
    Takes keyboard button, inline button with url (deeplink) or already str."""

    key = 'prefix_button'
    Button = Union[str, KeyboardButton, InlineKeyboardButton]

    def __init__(self, prefix_button: Union[Button, list[Button]]):
        super().__init__(prefix_button)

    async def check(self, msg: types.Message) -> Union[dict, bool]:
        for button_data in self.buttons_data:
            if msg.text.startswith(button_data):
                payload = msg.text.removeprefix(button_data)
                return {'payload': payload}
        return False


dp.bind_filter(CallbackQueryButton, event_handlers=[dp.callback_query_handlers])
dp.bind_filter(InlineQueryButton, event_handlers=[dp.inline_query_handlers])
dp.bind_filter(MessageButton, event_handlers=[dp.message_handlers])

dp.bind_filter(CallbackQueryPrefixButton, event_handlers=[dp.callback_query_handlers])
dp.bind_filter(InlineQueryPrefixButton, event_handlers=[dp.inline_query_handlers])
dp.bind_filter(MessagePrefixButton, event_handlers=[dp.message_handlers])

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
# msg2 = types.Message(text='/start send:bid:23')
#
# _filter = ButtonMessage(btn5)
# _filter = ButtonPrefixMessage(['1234', InlineKeyboardButton('122', url='https://t.me/bot?start=send:bid:')])
# _filter = ButtonPrefixMessage(['test:', 'error'])
# coro = _filter.check(msg1)  # error
# coro = _filter.check(msg2)
# coro = _filter.check(msg2)

# from asyncio import run

# print(run(coro))
