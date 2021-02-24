from aiogram import types

from keyboards import inline_funcs
from subfuncs.currents2 import Currents

__all__ = ['form_invite_project_article']


@Currents.set
async def form_invite_project_article(*, iquery: types.InlineQuery) -> types.InlineQueryResultArticle:
    """Form InlineQueryResultArticle [to invite to project] for current User."""
    text = 'Перейдите по ссылке, чтобы заполнить персональный проект'
    keyboard = inline_funcs.invite_project(iquery.from_user.id)
    imc = types.InputMessageContent(message_text=text)

    return types.InlineQueryResultArticle(
        id='0',
        title='Предложить проект',
        description='Нажмите, чтобы предложить личный проект вашему собеседнику',
        input_message_content=imc,
        reply_markup=keyboard,
    )
