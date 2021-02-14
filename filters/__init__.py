from loader import dp
from filters.check_prefixes import DeepLinkPrefix, QueryPrefix, InlinePrefix
from filters.for_groups import ProjectStatus, ChatUserRole, find_pair_chat

dp.filters_factory.bind(ProjectStatus, event_handlers=[dp.callback_query_handlers, dp.message_handlers])
dp.filters_factory.bind(ChatUserRole, event_handlers=[dp.callback_query_handlers, dp.message_handlers])
