"""Func and classes for Middlewares in main module."""

from dataclasses import dataclass
from typing import Awaitable, Callable, Optional

from aiogram import types

from loader import dp
from questions import ALL_CONV_STATES_GROUPS
from questions.misc import ConvStatesGroup, ConvStatesGroupMeta
from questions.misc import HandleException


@dataclass
class HandleResult:
    exception: Optional[HandleException]
    states_group: Optional[ConvStatesGroup]
    user_data: Optional[dict]


async def process_user_data(new_data: dict):
    # TODO: docs
    if new_data is None:
        return

    async with dp.current_state().proxy() as udata:
        for key, value in new_data.items():
            value_type = type(value)

            if value_type == list:
                udata.setdefault(key, [])
                udata[key].extend(value)

            elif value_type == tuple and not value:  # reset list if empty tuple passed
                udata[key] = []

            else:  # usual case
                udata[key] = value


async def process_exception(msg: types.Message, exception: HandleException):
    if not exception:
        return False

    e_body = exception.on_exception
    if isinstance(e_body, str):
        await msg.answer(e_body)
    elif isinstance(e_body, Awaitable):
        await e_body
    elif isinstance(e_body, Callable):
        await e_body(msg)

    return True


def get_states_group(state_name, result: HandleResult):
    """Return ConvStatesGroup or None."""
    cur_states_group = result.states_group

    if cur_states_group is None:  # if group is not explicitly specified
        for states_group, states_names in ALL_CONV_STATES_GROUPS.items():
            if state_name in states_names:
                cur_states_group = states_group
                break

    return cur_states_group


def parse_handle_results(results: list) -> HandleResult:
    """Parse results[0] to HandleResult."""
    exception, states_group, user_data = None, None, None

    if not results:
        return HandleResult(exception, states_group, user_data)

    result = results[0]
    if not isinstance(result, tuple):
        result = [result]

    for item in result:
        if isinstance(item, HandleException):
            exception = item
        elif isinstance(item, ConvStatesGroupMeta):
            states_group = item
        elif isinstance(item, dict):
            user_data = item

    return HandleResult(exception, states_group, user_data)