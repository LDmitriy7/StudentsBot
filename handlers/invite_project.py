from aiogram import types

from data_types.constants import TextQueries
from keyboards import inline_funcs, inline_plain
from loader import dp


@dp.inline_handler(text=TextQueries.INVITE_PROJECT)
async def send_project_invite_to_client(query: types.InlineQuery):
    text = 'Перейдите по ссылке, чтобы заполнить персональный проект'
    keyboard = inline_funcs.invite_project(query.from_user.id)
    imc = types.InputMessageContent(message_text=text)

    result = types.InlineQueryResultArticle(
        id='0',
        title='Предложить проект',
        description='Нажмите, чтобы предложить личный проект вашему собеседнику',
        input_message_content=imc,
        reply_markup=keyboard,
    )
    await query.answer([result], cache_time=0, is_personal=True)
