from aiogram import types
from aiogram.types import ContentType
import functions as funcs
from filters import find_pair_chat
from loader import dp
from texts import templates
from aiogram.utils.markdown import hbold as b


@dp.message_handler(find_pair_chat, content_types=ContentType.NEW_CHAT_MEMBERS)
async def send_project(msg: types.Message, user_id):
    """Отправляет вступившему пользователю данные о проекте."""
    project = await funcs.get_project_for_chat()
    if not project:
        return b('Этот проект уже закрыт!')

    is_client = user_id == project.client_id
    post_text = templates.form_post_text(project.status, project.data, with_note=is_client)
    await msg.answer(b('Текущий проект:'))
    await msg.answer(post_text)
    await funcs.send_files([tuple(f) for f in project.data.files])
    await msg.answer(b('Ожидайте собеседника...'))
