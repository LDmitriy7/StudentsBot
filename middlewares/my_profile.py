"""Post-Middleware after changing profile in worker_menu/my_profile."""
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from states import ChangeProfile
from aiogram.dispatcher import FSMContext
from middlewares.misc import check_on_exception
from functions import telegraph


class UpdatePage(BaseMiddleware):
    """Очищает состояние и обновляет личную страницу автора."""

    @staticmethod
    async def on_post_process_message(msg: types.Message, results: list, states_dict):
        if check_on_exception(results):
            return

        state_name = states_dict.get('raw_state')
        if state_name in ChangeProfile.all_states_names:
            state_ctx: FSMContext = states_dict['state']
            await state_ctx.finish()
            await telegraph.create_author_page(msg.from_user.id)
