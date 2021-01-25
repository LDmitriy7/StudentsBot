from collections import namedtuple
from typing import List, Union

from aiogram.dispatcher.filters.state import State, StatesGroup

QuestText = namedtuple('MessageText', ['text', 'keyboard'])
QuestFunc = namedtuple('MessageFunc', 'async_func')


class ConvStatesGroup(StatesGroup):
    """Class must contain only ConvState attributes. Will be used in ConvManager."""  # TODO: meta group
    pass


class ConvState(State):
    def __init__(self, question: Union[QuestText, QuestFunc, List[Union[QuestText, QuestFunc]]]):
        if not isinstance(question, List):
            question = [question]

        self.question: list = question
        super().__init__()
