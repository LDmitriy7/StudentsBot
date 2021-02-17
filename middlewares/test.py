from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

import functions as funcs
import subfuncs
from data_types.for_quests import ConvState, ConvStatesGroup, HandleException
from loader import dp


class PostMiddleware(BaseMiddleware):
    """."""

    @classmethod
    async def on_post_process_message(cls, msg: types.Message, results: list, state_dict: dict):
        raise NotImplemented

    @classmethod
    async def on_post_process_callback_query(cls, query: types.CallbackQuery, results: list, state_dict: dict):
        msg = query.message
        await query.answer()
        await cls.on_post_process_message(msg, results, state_dict)


class UserDataUpdater(PostMiddleware):

    @classmethod
    async def on_post_process_message(cls, msg: types.Message, results: list, *args):
        new_data = subfuncs.recursive_search_obj(dict, results)
        if new_data:
            await funcs.update_user_data(new_data)


class SwitchConvState(PostMiddleware):

    @classmethod
    async def on_post_process_message(cls, msg: types.Message, results: list, *args):
        state_name = await dp.current_state().get_state()
        conv_state = subfuncs.get_state_by_name(state_name, ConvStatesGroup)
        new_conv_group = subfuncs.recursive_search_obj(ConvStatesGroup.__class__, results)
        exception = subfuncs.recursive_search_obj(HandleException, results)

        if exception:
            await funcs.process_exception(exception)
        else:
            if new_conv_group:
                await new_conv_group.first()
            elif conv_state:
                await conv_state.group.next()


class AskQuestion(PostMiddleware):
    @classmethod
    async def on_post_process_message(cls, msg: types.Message, results: list, *args):
        state_name = await dp.current_state().get_state()
        conv_state = subfuncs.get_state_by_name(state_name, ConvStatesGroup)
        if conv_state:
            conv_state: ConvState
            await funcs.ask_question(conv_state.question)
        else:
            await dp.current_state().finish()
