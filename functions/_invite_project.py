from aiogram import types

from keyboards import inline_funcs
from aiogram.contrib.currents import SetCurrent

__all__ = ['form_invite_project_article']


@SetCurrent.inline_query
async def form_invite_project_article(*, query: types.InlineQuery) -> types.InlineQueryResultArticle:
    """Form InlineQueryResultArticle [to invite to project] for current User."""
    text = 'Перейдите по ссылке, чтобы заполнить персональный проект'
    keyboard = inline_funcs.invite_project(query.from_user.id)
    imc = types.InputMessageContent(message_text=text)

    return types.InlineQueryResultArticle(
        id='0',
        title='Предложить проект',
        description='Нажмите, чтобы предложить личный проект вашему собеседнику',
        input_message_content=imc,
        reply_markup=keyboard,
    )
