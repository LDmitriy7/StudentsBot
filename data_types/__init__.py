"""Классы без внешних зависимостей."""

from data_types.common import Update, KeyboardMarkup, Awaitable, AsyncFunction
from data_types.constants import Prefixes, ProjectStatuses, UserRoles, SendTo
from data_types.for_quests import QuestFunc, QuestText, Quest, ExceptionBody, HandleException
from data_types.for_quests import ConvState, ConvStatesGroup, ConvStatesGroupMeta

# common - общее
# states - только обычные группы состояний
# constants - сгрупированные в классы константы
# for_quests - все для состояний с вопросами
# dataclasses - классы с набором данных
