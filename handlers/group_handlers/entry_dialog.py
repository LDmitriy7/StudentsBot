from aiogram import html, types
from aiogram.types import ContentType

import functions as funcs
import texts
from filters import find_pair_chat
from loader import dp, users_db
from texts import templates


@dp.message_handler(find_pair_chat, content_types=ContentType.NEW_CHAT_MEMBERS)
async def send_project(msg: types.Message, user_id: int, pchat_id: int):
    """Отправляет вступившему пользователю данные о проекте."""
    project = await funcs.get_project_for_chat()
    if not project:
        return html.b('Этот проект уже закрыт!')

    text = texts.welcome_group

    is_client = user_id == project.client_id

    if is_client:
        pchat = await users_db.get_chat_by_id(pchat_id)
        worker_account = await users_db.get_account_by_id(pchat.user_id)
        text += html.b('Исполнитель - ') + html.a(worker_account.profile.nickname, worker_account.page_url)

    await msg.answer(text)

    post_text = templates.form_post_text(project.status, project.data, with_note=is_client)
    await msg.answer(html.b('Текущий проект:\n') + post_text)
    await funcs.send_files([tuple(f) for f in project.data.files])

    await msg.answer(html.b('Ожидайте собеседника...'))
