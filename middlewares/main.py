from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from middlewares.misc import ask_question, get_states_group, parse_handle_results, process_exception, process_user_data
from questions import ALL_CONV_STATES
from questions.misc import ConvState


class ConvManager(BaseMiddleware):
    """Conversation Manager."""  # TODO: docs

    @classmethod
    async def on_post_process_message(cls, msg: types.Message, results: list, state_dict: dict):
        state_ctx, state_name = state_dict.get('state'), state_dict.get('raw_state')

        result = parse_handle_results(results)
        states_group = get_states_group(state_name, result)

        await process_user_data(state_ctx, result.user_data)  # update data if exists

        if states_group is None:  # user not in conversation
            return

        if await process_exception(msg, result.exception):  # exit with exception
            return

        new_state_name = await states_group.next()
        new_state: ConvState = ALL_CONV_STATES[new_state_name]

        await ask_question(msg, new_state.question)

    @classmethod
    async def on_post_process_callback_query(cls, query: types.CallbackQuery, results: list, state_dict: dict):
        msg = query.message
        await cls.on_post_process_message(msg, results, state_dict)
