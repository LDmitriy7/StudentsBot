from aiogram import types

from keyboards import inline_funcs

__all__ = ['make_offer_project_article']


def make_offer_project_article(project_id) -> types.InlineQueryResultArticle:
    text = 'Предлагаю вам персональный проект'
    keyboard = inline_funcs.pick_project(project_id)
    imc = types.InputMessageContent(message_text=text)

    return types.InlineQueryResultArticle(
        id='0',
        title='Предложить проект',
        description='Нажмите, чтобы предложить личный проект вашему собеседнику',
        input_message_content=imc,
        reply_markup=keyboard,
    )
