from aiogram import types
from aiogram.dispatcher import FSMContext
from texts import templates
from questions.misc import HandleException


async def send_project(msg: types.Message, state: FSMContext):
    """Return worker, post_msg and post_data"""
    post_data = await state.get_data()
    post_text = templates.form_post_text(post_data)

    worker = post_data['worker']
    text1 = f'Заказчик ({msg.from_user.full_name}) предложил вам проект:'

    try:
        await msg.bot.send_message(worker, text1)
        post_msg = await msg.bot.send_message(worker, post_text)  # отправка проекта
    except:
        return HandleException('Не могу отправить этому исполнителю')

    return worker, post_msg, post_data
