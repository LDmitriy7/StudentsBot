"""Classes-decorators for passing current ctx_type instances and derivatives to functions."""

from __future__ import annotations

import functools
import inspect
from typing import Optional

from aiogram import types, Dispatcher as _Dispatcher, Bot as _Bot
from aiogram.dispatcher.filters.state import State as _State, StatesGroup
from aiogram.utils.mixins import ContextInstanceMixin


def get_state_by_name(state_name: str) -> Optional[_State]:
    """Search for State with state_name in all StatesGroups."""
    for state_group in StatesGroup.__subclasses__():
        for state in state_group.all_states:
            if state.state == state_name:
                return state


async def get_sdata(obj: _Dispatcher) -> dict:
    try:
        return await obj.current_state().get_data()
    except AttributeError:
        return {}


async def get_raw_state(obj: _Dispatcher) -> Optional[str]:
    try:
        return await obj.current_state().get_state()
    except AttributeError:
        return None


async def get_state(obj: _Dispatcher) -> Optional[_State]:
    try:
        raw_state = await obj.current_state().get_state()
        return get_state_by_name(raw_state)
    except AttributeError:
        return None


class ContextObj:

    def __init__(self, ctx_type: type[ContextInstanceMixin], get_target: callable = lambda x: x):
        self.ctx_type = ctx_type
        self.get_target = get_target

    async def get_current(self):
        try:
            obj = self.ctx_type.get_current()

            target = self.get_target(obj)
            if inspect.isawaitable(target):
                target = await target

            return target
        except AttributeError:
            return None

    def __repr__(self):
        return f'ContextObj(Type={self.ctx_type.__name__}, Target={self.get_target.__name__})'


class Currents:
    user = ContextObj(types.User)
    chat = ContextObj(types.Chat)
    query = ContextObj(types.CallbackQuery)
    iquery = ContextObj(types.InlineQuery)
    msg = ContextObj(types.Message)
    dp = ContextObj(_Dispatcher)
    bot = ContextObj(_Bot)

    sdata = ContextObj(_Dispatcher, get_sdata)
    raw_state = ContextObj(_Dispatcher, get_raw_state)
    # state = ContextObj(_Dispatcher, get_state)

    user_id = ContextObj(types.User, lambda obj: obj.id)
    user_name = ContextObj(types.User, lambda obj: obj.full_name)
    username = ContextObj(types.User, lambda obj: obj.username)
    chat_id = ContextObj(types.Chat, lambda obj: obj.id)
    chat_type = ContextObj(types.Chat, lambda obj: obj.type)

    inline_msg_id = ContextObj(types.CallbackQuery, lambda obj: obj.inline_message_id)
    query_msg = ContextObj(types.CallbackQuery, lambda obj: obj.message)
    data = ContextObj(types.CallbackQuery, lambda obj: obj.data)
    text = ContextObj(types.Message, lambda obj: obj.text)

    @classmethod
    def set(cls, async_func):
        @functools.wraps(async_func)
        async def wrapper(*args, **kwargs):
            argspec = inspect.getfullargspec(async_func)

            # update not passed kwargs
            for arg in argspec.kwonlyargs:
                if arg in cls.keywords() and arg not in kwargs:
                    obj: ContextObj = getattr(cls, arg)
                    kwargs[arg] = await obj.get_current()

            return await async_func(*args, **kwargs)

        return wrapper

    @classmethod
    def keywords(cls) -> set[str]:
        return {k for k, v in vars(cls).items() if isinstance(v, ContextObj)}


if __name__ == '__main__':
    from asyncio import get_event_loop

    loop = get_event_loop()

    types.User.set_current(types.User(id=123, username='LDM7'))
    types.Chat.set_current(types.Chat(type='private'))
    types.Message.set_current(types.Message(id=1))


    @Currents.set
    async def test2(*, chat_type, query):
        print(locals())


    loop.run_until_complete(test2())
