from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger

from loader import dp
from middlewares.misc import get_states_group, parse_handle_results, process_exception, process_user_data
from questions import ALL_CONV_STATES
from questions.misc import ConvState, ask_question


class ConvManager(BaseMiddleware):
    """Conversation Manager."""  # TODO: docs

    @classmethod
    async def on_post_process_message(cls, msg: types.Message, results: list, *args):
        state_name = await dp.current_state().get_state()

        result = parse_handle_results(results)
        states_group = get_states_group(state_name, result)

        await process_user_data(result.user_data)  # update data if exists
        logger.info('AFTER | StateGroup - {}, NewData - {}', states_group, result.user_data)

        if await process_exception(msg, result.exception):  # exit with exception
            logger.info('EXCEPTION: {}', result.exception)
            return

        if states_group:  # user in conversation
            new_state_name = await states_group.next()

            if not new_state_name:  # user finished conversation
                await dp.current_state().finish()
                return

            new_state: ConvState = ALL_CONV_STATES[new_state_name]
            await ask_question(msg, new_state.question)
            logger.info('EXIT | NewState - {}, Quest - {}', new_state_name, new_state.question)

    @classmethod
    async def on_post_process_callback_query(cls, query: types.CallbackQuery, results: list, state_dict: dict):
        msg = query.message
        await query.answer()
        await cls.on_post_process_message(msg, results, state_dict)
