"""All classes for making questions."""

from dataclasses import dataclass
from typing import Awaitable, Callable, List, TypeVar, Union

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup, StatesGroupMeta

KeyboardMarkup = TypeVar('KeyboardMarkup', types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup)
AsyncFunction = TypeVar('AsyncFunction', bound=Callable[[types.Message], Awaitable])


@dataclass
class QuestText:
    text: str
    keyboard: KeyboardMarkup


@dataclass
class QuestFunc:
    async_func: AsyncFunction


Quest = TypeVar('Quest', QuestText, QuestFunc)


class HandleException:
    def __init__(self, on_exception: Union[None, str, Awaitable, AsyncFunction] = None):
        self.on_exception = on_exception


class ConvState(State):
    """All States must have question attr. It will be used in ConvManager."""

    def __init__(self, question: Union[Quest, List[Quest]]):
        if not isinstance(question, list):
            question = [question]

        self.question = question
        super().__init__()


class ConvStatesGroupMeta(StatesGroupMeta):
    def __new__(mcs, class_name, bases, namespace, **kwargs):
        for prop in namespace.values():
            if type(prop) is State:
                raise TypeError(f'{class_name} attrs can be instance of ConvState, not State')

        return super().__new__(mcs, class_name, bases, namespace)


class ConvStatesGroup(StatesGroup, metaclass=ConvStatesGroupMeta):
    """Class attrs must be ConvState instances. All subclasses will be used in ConvManager."""
