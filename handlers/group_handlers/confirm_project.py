from loader import dp, users_db, bot
from keyboards.inline_funcs import GroupMenuKeyboard
from keyboards import inline_funcs
from datatypes import ProjectStatuses, UserRoles, Prefixes
from aiogram import types
from filters import find_pair_chat, QueryPrefix


@dp.callback_query_handler(text=GroupMenuKeyboard.CONFIRM_PROJECT, pstatus=ProjectStatuses.IN_PROGRESS,
                           user_role=UserRoles.CLIENT)
async def ask_confirm_project(query: types.CallbackQuery):
    msg = query.message
    chat = await users_db.get_chat_by_id(msg.chat.id)
    text = 'Вы точно хотите подтвердить выполнение проекта?'
    keyboard = inline_funcs.total_confirm_project(chat.project_id)
    await msg.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(find_pair_chat, QueryPrefix(Prefixes.CONFIRM_PROJECT_),
                           pstatus=ProjectStatuses.IN_PROGRESS, user_role=UserRoles.CLIENT)
async def confirm_project(query: types.CallbackQuery, pchat_id: int, payload: str):
    msg = query.message
    project = await users_db.get_project_by_id(payload)

    await users_db.update_project_status(payload, ProjectStatuses.COMPLETED)
    await users_db.incr_balance(project.worker_id, project.data.price)

    client_text = '<b>Теперь вы можете написать отзыв</b>'
    worker_text = 'Заказчик подтвердил выполнение проекта, деньги перечислены на ваш счет.'
    await msg.answer(client_text)
    await bot.send_message(pchat_id, worker_text)
