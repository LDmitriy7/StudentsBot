"""Custom filters for checking on prefix in update's text/data."""
from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery, InlineQuery


class DeepLinkPrefix:
    """Check deep-link for prefix, return payload without prefix."""

    def __init__(self, dprefix: str):
        self.dprefix = dprefix

    def __call__(self, msg: types.Message) -> Union[dict, bool]:
        deeplink = msg.text.split()
        if deeplink[0] == '/start' and deeplink[-1].startswith(self.dprefix):
            payload = deeplink[-1].removeprefix(self.dprefix)
            return {'payload': payload}
        return False


class QueryPrefix:
    """Check query.data for prefix, return payload without prefix."""

    def __init__(self, qprefix: str):
        self.qprefix = qprefix

    def __call__(self, query: types.CallbackQuery) -> Union[dict, bool]:
        if query.data.startswith(self.qprefix):
            payload = query.data.removeprefix(self.qprefix)
            return {'payload': payload}
        return False


class InlinePrefix:
    """Check query.query for prefix, return payload without prefix."""

    def __init__(self, iprefix: str):
        self.iprefix = iprefix

    def __call__(self, query: types.InlineQuery) -> Union[dict, bool]:
        if query.query.startswith(self.iprefix):
            payload = query.query.removeprefix(self.iprefix)
            return {'payload': payload}
        return False


class Prefix(BoundFilter):
    """Check deeplink (in msg.text), query.data or query.query for prefix;
    return payload without prefix."""

    key = 'prefix'

    def __init__(self, prefix: str):
        self.prefix = prefix

    async def check(self, obj: Union[Message, CallbackQuery, InlineQuery]) -> Union[dict, bool]:
        if isinstance(obj, Message):
            command, _, deeplink = obj.text.partition(' ')
            if command == '/start' and deeplink.startswith(self.prefix):
                payload = deeplink.removeprefix(self.prefix)
                return {'payload': payload}
        elif isinstance(obj, CallbackQuery):
            if obj.data.startswith(self.prefix):
                payload = obj.data.removeprefix(self.prefix)
                return {'payload': payload}
        elif isinstance(obj, InlineQuery):
            if obj.query.startswith(self.prefix):
                payload = obj.query.removeprefix(self.prefix)
                return {'payload': payload}
        return False
