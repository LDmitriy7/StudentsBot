from filters.for_groups import ProjectStatus, ChatUserRole, find_pair_chat
from loader import dp

from filters import button_filters  # ?


def setup(filters: list):
    event_handlers = [dp.callback_query_handlers, dp.message_handlers]
    for item in filters:
        dp.filters_factory.bind(item, event_handlers=event_handlers)


setup([ProjectStatus, ChatUserRole])
