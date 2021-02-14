from aiogram import types

from filters import find_pair_chat
import functions as funcs
from loader import bot, dp
from texts import templates


@dp.message_handler(find_pair_chat, content_types='new_chat_members')
async def send_welcome(msg: types.Message, pchat_id: int):
    """Отправляет вступившему данные о проекте, уведомляет собеседника."""
    project = await funcs.get_project_for_chat(msg.chat)
    is_client = msg.from_user.id == project.client_id  # является ли заказчиком проекта
    post_text = templates.form_post_text(project.status, project.data, with_note=is_client)
    files = project.data.files

    await msg.answer('<b>Текущий проект:</b>')
    await msg.answer(post_text)
    await msg.answer('<b>Ожидайте собеседника...</b>')
    await bot.send_message(pchat_id, '<b>Ваш собеседник вступил в чат. Напишите ему первым.</b>')


@dp.message_handler(find_pair_chat, content_types='left_chat_member')
async def send_bye(msg: types.Message, pchat_id: int):
    """Отправляет уведомление о выходе собеседника из чата."""
    await bot.send_message(pchat_id, '<b>Ваш собеседник покинул группу.</b>')


@dp.message_handler(find_pair_chat, content_types='any')
async def forward(msg: types.Message, pchat_id: int):
    """Копирует все сообщения в связанную группу."""
    await msg.copy_to(pchat_id)
