"""Post-Middleware after changing profile in worker_menu/my_profile."""
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from states import ChangeProfile, MiscStates
from aiogram.dispatcher import FSMContext
from middlewares.misc import check_on_exception
import functions as funcs


class UpdatePage(BaseMiddleware):
    """Очищает состояние и обновляет личную страницу автора."""

    ALL_STATE_NAMES = [*ChangeProfile.all_states_names, MiscStates.change_subjects.state]

    @classmethod
    async def on_post_process_message(cls, msg: types.Message, results: list, states_dict):
        if check_on_exception(results):
            return

        state_name = states_dict.get('raw_state')
        if state_name in cls.ALL_STATE_NAMES:
            state_ctx: FSMContext = states_dict['state']
            await state_ctx.finish()
            await funcs.create_author_page(msg.from_user.id)
