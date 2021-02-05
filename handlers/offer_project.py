from loader import dp
from aiogram import types
from keyboards import inline_funcs, inline_plain


@dp.inline_handler(text=inline_plain.OFFER_PROJECT_TO_CLIENT_QUERY)
async def send_offer_to_client(query: types.InlineQuery):
    worker_id = query.from_user.id
    text = 'Перейдите по ссылке, чтобы заполнить персональный проект'
    keyboard = inline_funcs.offer_project_to_client(worker_id)
    imc = types.InputMessageContent(message_text=text)

    result = types.InlineQueryResultArticle(
        id='0',
        title='Предложить проект',
        description='Нажмите, чтобы предложить личный проект вашему собеседнику',
        input_message_content=imc,
        reply_markup=keyboard,
    )
    await query.answer([result], cache_time=0, is_personal=True)
