"""Post-Middleware after changing profile in worker_menu."""
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

import functions as funcs
from questions import ChangeProfile, FeedbackConv


class UpdatePage(BaseMiddleware):
    """Update personal user's page."""

    FIT_STATE_NAMES = [*ChangeProfile.states_names, FeedbackConv.ask_text.state]

    @classmethod
    async def on_post_process_message(cls, msg: types.Message, results: list, states_dict: dict):
        state_name = states_dict.get('raw_state')
        if state_name in cls.FIT_STATE_NAMES:
            await funcs.save_author_page()
