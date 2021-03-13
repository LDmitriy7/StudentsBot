from aiogram.contrib.questions import QuestText
from aiogram import html

import functions as funcs
import keyboards as KB
from data_types import ProjectStatuses, UserRoles
from filters import find_pair_chat
from loader import dp, users_db, bot


@dp.callback_query_handler(text=KB.GroupMenu.CONFIRM_PROJECT,
                           pstatus=ProjectStatuses.IN_PROGRESS,
                           user_role=UserRoles.client)
async def ask_confirm_project(chat_id):
    chat = await users_db.get_chat_by_id(chat_id)
    text = 'Вы точно хотите подтвердить выполнение проекта?'
    keyboard = KB.ConfirmProject(chat.project_id)
    return QuestText(text, keyboard)


@dp.callback_query_handler(find_pair_chat,
                           button=KB.ConfirmProject.CONFIRM,
                           pstatus=ProjectStatuses.IN_PROGRESS,
                           user_role=UserRoles.client)
async def confirm_project(pchat_id: int, suffix: str):
    project = await users_db.get_project_by_id(suffix)
    project.status = ProjectStatuses.COMPLETED

    await users_db.update_project_status(suffix, project.status)
    await users_db.incr_profile_deals_amount(project.worker_id)
    await funcs.update_post(project.id, project.status, project.post_url, project.data)
    await users_db.incr_balance(project.worker_id, int(project.data.price * 0.9))

    worker_text = html.b('Заказчик подтвердил выполнение проекта, деньги перечислены на ваш счет.')
    await bot.send_message(pchat_id, worker_text)
    return html.b('Теперь вы можете написать отзыв')
