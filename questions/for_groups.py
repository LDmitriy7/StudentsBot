from aiogram.contrib.questions import SingleConvStatesGroup, ConvState, QuestText
from aiogram.types import ForceReply

ask_work_price = 'Введите цену в гривнах'


class ForGroups(SingleConvStatesGroup):
    ask_work_price = ConvState(ask_work_price)
