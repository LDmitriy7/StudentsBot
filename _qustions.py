from dataclasses import dataclass
from typing import Union
import inspect
from aiogram.dispatcher.filters.state import State, StatesGroupMeta, StatesGroup

from datatypes import KeyboardMarkup, AsyncFunction


@dataclass
class QuestText:
    text: str
    keyboard: KeyboardMarkup

    def __repr__(self):
        return f'QText({self.text}, {self.keyboard})'


@dataclass
class QuestFunc:
    async_func: AsyncFunction

    def __repr__(self):
        return f'QFunc({self.async_func})'


Quest = Union[QuestText, QuestFunc]


class ConvState(State):
    """All States must have question attr. It will be used in ConvManager."""

    def __init__(self, question: Union[Quest, list[Quest]]):
        if not isinstance(question, list):
            question = [question]

        self.question = question
        super().__init__()


class ConvStatesGroupMeta(StatesGroupMeta):
    def __new__(mcs, class_name, bases, namespace, **kwargs):
        for prop in namespace.values():
            if not isinstance(prop, ConvState):
                raise TypeError(f'{class_name} attrs must be instance of {ConvState}')

        return super().__new__(mcs, class_name, bases, namespace)


class ConvStatesGroup(StatesGroup, metaclass=ConvStatesGroupMeta):
    """Class attrs must be ConvState instances."""

