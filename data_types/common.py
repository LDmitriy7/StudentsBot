from typing import Union, Callable, Awaitable

from aiogram import types

Update = Union[types.Message, types.CallbackQuery]
KeyboardMarkup = Union[types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup]
AsyncFunction = Callable[[], Awaitable]
ExceptionBody = Union[None, str, Awaitable, AsyncFunction]
