from aiogram import types
from aiogram.dispatcher import FSMContext
from texts import templates
from questions.misc import HandleException
from loader import bot
from keyboards import inline_funcs, markup
from typing import Union, Optional
from type_classes import PairChats


async def send_invitation(client_name: str, worker_id: int, chat_link: str) -> Optional[HandleException]:
    """Try to send invitation to worker, return Message or HandleException."""
    text = f'Заказчик ({client_name}) предложил вам личный проект'
    keyboard = inline_funcs.link_button('Перейти в чат', chat_link)

    try:
        await bot.send_message(worker_id, text, reply_markup=keyboard)
    except:
        return HandleException('Не могу отправить этому исполнителю')


async def try_send_project(msg: types.Message, worker_id: int, worker_chat_link: str) -> bool:
    """Try to send project to worker, return True on success."""
    result = await send_invitation(msg.from_user.full_name, worker_id, worker_chat_link)
    if isinstance(result, HandleException):  # распространяем исключение
        return False

    keyboard = inline_funcs.link_button('Перейти в чат', worker_chat_link)
    await msg.answer('Проект отправлен', reply_markup=markup.main_kb)
    await msg.answer('Ожидайте исполнителя в чате', reply_markup=keyboard)
    return True
