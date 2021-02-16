from dataclasses import dataclass
from typing import Union

from aiogram.dispatcher.filters.state import State, StatesGroupMeta, StatesGroup

from data_types.common import KeyboardMarkup, AsyncFunction, ExceptionBody


@dataclass
class HandleException:
    on_exception: ExceptionBody = None

    def __repr__(self):
        return f'{self.on_exception}'


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
    """States with question attribute. It should be used to ask next question in conversation."""

    def __init__(self, question: Union[Quest, list[Quest]]):
        if not isinstance(question, list):
            question = [question]

        self.question = question
        super().__init__()


class ConvStatesGroupMeta(StatesGroupMeta):
    def __new__(mcs, class_name, bases, namespace, **kwargs):
        for prop in namespace.values():
            if isinstance(prop, State) and not isinstance(prop, ConvState):
                err_text = f'{class_name} attrs must be instance of {ConvState.__name__}, not {State.__name__}'
                raise TypeError(err_text)

        return super().__new__(mcs, class_name, bases, namespace)


class ConvStatesGroup(StatesGroup, metaclass=ConvStatesGroupMeta):
    """StatesGroup with ConvState instances attributes (not State)."""
