from filters.check_prefixes import DeepLinkPrefix, QueryPrefix, InlinePrefix
from filters.common import StorageData
from filters.for_groups import ProjectStatus, ChatUserRole, find_pair_chat
from loader import dp


def setup(filters: list):
    event_handlers = [dp.callback_query_handlers, dp.message_handlers]
    for item in filters:
        dp.filters_factory.bind(item, event_handlers=event_handlers)


setup([ProjectStatus, ChatUserRole, StorageData])
