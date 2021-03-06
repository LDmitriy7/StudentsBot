from aiogram import types, html
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.contrib.questions import QuestText

import functions as funcs
import keyboards as KB
from data_types import ProjectStatuses, UserRoles
from filters import find_pair_chat
from loader import dp, users_db, bot
from questions import ForGroups as States


@dp.callback_query_handler(find_pair_chat,
                           text=KB.GroupMenu.OFFER_PRICE,
                           pstatus=ProjectStatuses.ACTIVE,
                           user_role=UserRoles.worker)
async def ask_work_price():
    return UpdateData(new_state=States.ask_work_price)


@dp.message_handler(find_pair_chat,
                    state=States.ask_work_price,
                    pstatus=ProjectStatuses.ACTIVE,
                    user_role=UserRoles.worker)
async def offer_price(text, chat_id, pchat_id: int):
    if not text.isdigit():
        return 'Ошибка, отправьте число'

    price = int(text)
    chat = await users_db.get_chat_by_id(chat_id)
    client_text = f'Автор предлагает вам сделку за <b>{price} грн</b>'
    keyboard = KB.PayForProject(price, chat.project_id)
    await bot.send_message(pchat_id, client_text, reply_markup=keyboard)
    return UpdateData(on_conv_exit='Заявка отправлена, мы пришлем вам уведомление в случае оплаты.')


@dp.callback_query_handler(find_pair_chat,
                           button=KB.PayForProject.PAY,
                           pstatus=ProjectStatuses.ACTIVE,
                           user_role=UserRoles.client)
async def pay_for_project(user_id, chat_id, pchat_id: int, suffix: str):
    client_balance = await funcs.get_account_balance()
    price, project_id = suffix.split('_')
    price = int(price)

    if price <= client_balance:
        worker_chat = await users_db.get_chat_by_id(pchat_id)
        await funcs.start_project_update(project_id, price, user_id, worker_chat.user_id, chat_id, pchat_id)
        await bot.send_message(pchat_id, html.b('Проект оплачен, приступайте к работе'))
        return html.b('Проект оплачен, уведомление отправлено автору')
    else:
        text = f'У вас не хватает {price - client_balance} грн.' \
               f' Отправьте недостающую сумму через один из банков. Обязательно укажите {user_id} в комментарии'
        return QuestText(text, KB.payment)


@dp.callback_query_handler(find_pair_chat,
                           button=KB.PayForProject.REFUSE,
                           pstatus=ProjectStatuses.ACTIVE,
                           user_role=UserRoles.client)
async def refuse_work_price(msg: types.Message, pchat_id: int):
    await msg.delete()
    await bot.send_message(pchat_id, html.b('Заказчик отказался от предложенной цены'))
