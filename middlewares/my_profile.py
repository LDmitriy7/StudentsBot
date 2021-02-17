"""Post-Middleware after changing profile in worker_menu/my_profile."""
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware
from data_types.states import ChangeProfile, MiscStates
from data_types import HandleException

import functions as funcs
import subfuncs


class UpdatePage(BaseMiddleware):
    """Очищает состояние и обновляет личную страницу автора."""

    FIT_STATE_NAMES = [*ChangeProfile.states_names, MiscStates.change_subjects]

    @classmethod
    async def on_post_process_message(cls, msg: types.Message, results: list, states_dict):
        if subfuncs.recursive_search_obj(HandleException, results):
            return

        state_name = states_dict.get('raw_state')
        if state_name in cls.FIT_STATE_NAMES:
            state_ctx: FSMContext = states_dict['state']
            await state_ctx.finish()
            await funcs.create_author_page()
