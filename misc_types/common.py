from dataclasses import dataclass
from typing import Union, Callable, Awaitable, Optional

from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroupMeta

Update = Union[types.Message, types.CallbackQuery]
KeyboardMarkup = Union[types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup]
AsyncFunction = Callable[[], Awaitable]


@dataclass
class HandleException:
    on_exception: Union[None, str, Awaitable, AsyncFunction] = None

    def __repr__(self):
        return f'{self.on_exception}'


@dataclass
class HandleResult:
    exception: Optional[HandleException]
    states_group: Optional[StatesGroupMeta]
    user_data: Optional[dict]
