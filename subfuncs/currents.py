from __future__ import annotations

import functools
from typing import Awaitable, Callable, Optional

from aiogram import types, Dispatcher, Bot as _Bot
from aiogram.dispatcher.filters.state import State as _State, StatesGroup
from aiogram.utils.mixins import ContextInstanceMixin

AsyncFunction = Callable[..., Awaitable]


def _get_state_by_name(state_name: str) -> Optional[_State]:
    """Search for State with state_name in all StatesGroups."""
    for state_group in StatesGroup.__subclasses__():
        for state in state_group.all_states:
            if state.state == state_name:
                return state


class CurrentType:
    """Decorator[AsyncFunction] -> AsyncFunction

    For function(*, {key}=None):
    if {key} is None, set {key} = current ctx_type instance or derivatives
    """

    ctx_type: type[ContextInstanceMixin] = ...
    key: str = ...

    @staticmethod
    async def fetch_attr(obj: ctx_type):
        """Fetch attribute of current object instead of object itself."""
        return obj

    def __new__(cls, async_func, ctx_type=ctx_type, key=key):
        @functools.wraps(async_func)
        async def wrapper(*args, **kwargs):
            key_value = kwargs.get(cls.key)

            if key_value is None:
                key_value = await cls.fetch_attr(cls.ctx_type.get_current())

            kwargs[cls.key] = key_value
            return await async_func(*args, **kwargs)

        return wrapper


class User(CurrentType):
    ctx_type = types.User
    key = 'user'


class Chat(CurrentType):
    ctx_type = types.Chat
    key = 'chat'


class Query(CurrentType):
    ctx_type = types.CallbackQuery
    key = 'query'


class InlineQuery(CurrentType):
    ctx_type = types.InlineQuery
    key = 'query'


class Message(CurrentType):
    ctx_type = types.Message
    key = 'msg'


class Dp(CurrentType):
    ctx_type = Dispatcher
    key = 'dp'


class Bot(CurrentType):
    ctx_type = _Bot
    key = 'bot'


class Udata(CurrentType):
    ctx_type = Dispatcher
    key = 'udata'

    @staticmethod
    async def fetch_attr(obj: ctx_type):
        try:
            return await obj.current_state().get_data()
        except AttributeError:
            return None


class RawState(CurrentType):
    ctx_type = Dispatcher
    key = 'state'

    @staticmethod
    async def fetch_attr(obj: ctx_type):
        try:
            return await obj.current_state().get_state()
        except AttributeError:
            return None


class State(CurrentType):
    ctx_type = Dispatcher
    key = 'state'

    @staticmethod
    async def fetch_attr(obj: ctx_type):
        try:
            raw_state = await obj.current_state().get_state()
            return _get_state_by_name(raw_state)
        except AttributeError:
            return None


# ---
class UserID(User):
    key = 'user_id'

    @staticmethod
    async def fetch_attr(obj: User.ctx_type):
        return obj.id


class UserName(User):
    key = 'user_name'

    @staticmethod
    async def fetch_attr(obj: User.ctx_type):
        return obj.full_name


class UserUname(User):
    key = 'username'

    @staticmethod
    async def fetch_attr(obj: User.ctx_type):
        return obj.username


# ---
class ChatID(Chat):
    key = 'chat_id'

    @staticmethod
    async def fetch_attr(obj: Chat.ctx_type):
        return obj.id


class ChatType(Chat):
    key = 'chat_type'

    @staticmethod
    async def fetch_attr(obj: Chat.ctx_type):
        return obj.type


if __name__ == '__main__':
    from asyncio import get_event_loop
    from loader import dp


    class T(StatesGroup):
        ask_price = _State()


    loop = get_event_loop()

    types.User.set_current(types.User(id=123, username='LDM7'))
    Dispatcher.set_current(dp)
    loop.run_until_complete(Dispatcher.get_current().current_state().set_state('T:ask_price'))


    @User
    @Dp
    @Message
    @Chat
    @Query
    @InlineQuery
    @Bot
    @Udata
    @RawState
    @State
    @UserID
    @UserName
    @UserUname
    @ChatType
    async def test(**kwargs):
        print(kwargs)


    loop.run_until_complete(test())
