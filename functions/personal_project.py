from aiogram import types
from aiogram.dispatcher import FSMContext
from texts import templates
from questions.misc import HandleException
from loader import bot
from keyboards import inline_funcs
from typing import Union


async def send_project(client_name: str, post_data: dict) -> Union[types.Message, HandleException]:
    """Try to send project to worker, return Message or HandleException."""
    worker_id = post_data['worker_id']
    text = f'Заказчик ({client_name}) предложил вам личный проект'

    try:
        return await bot.send_message(worker_id, text)
    except:
        return HandleException('Не могу отправить этому исполнителю')


async def add_post_keyboard(post_msg: types.Message, wchat_link: str):
    """Add button with worker chat link."""
    keyboard = inline_funcs.link_button('Перейти в чат', wchat_link)
    await post_msg.edit_reply_markup(keyboard)
