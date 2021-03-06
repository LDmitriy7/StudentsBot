from aiogram import types
from aiogram.dispatcher.currents import CurrentObjects

import keyboards as KB

__all__ = ['form_invite_project_article']


@CurrentObjects.decorate
async def form_invite_project_article(*, user_id) -> types.InlineQueryResultArticle:
    """Form InlineQueryResultArticle [to invite to project] for current User."""
    text = 'Перейдите по ссылке, чтобы заполнить персональный проект'
    keyboard = KB.InviteProject(user_id)
    imc = types.InputMessageContent(message_text=text)

    return types.InlineQueryResultArticle(
        id='0',
        title='Предложить проект',
        description='Нажмите, чтобы предложить личный проект вашему собеседнику',
        input_message_content=imc,
        reply_markup=keyboard,
    )
