from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.utils.markdown import hbold as b

import functions as funcs
from data_types import ProjectStatuses, UserRoles, Prefixes, TextQueries
from filters import find_pair_chat
from keyboards import inline_funcs
from keyboards.inline_funcs import GroupMenu
from loader import dp, users_db, bot
from questions import ForGroups as States


@dp.callback_query_handler(find_pair_chat,
                           text=GroupMenu.OFFER_PRICE,
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
    keyboard = inline_funcs.pay_for_project(price, chat.project_id)
    await bot.send_message(pchat_id, client_text, reply_markup=keyboard)
    return UpdateData(on_conv_exit='Заявка отправлена, мы пришлем вам уведомление в случае оплаты.')


@dp.callback_query_handler(find_pair_chat,
                           cprefix=Prefixes.PAY_FOR_PROJECT_,
                           pstatus=ProjectStatuses.ACTIVE,
                           user_role=UserRoles.client)
async def pay_for_project(user_id, chat_id, pchat_id: int, payload: str):
    client_balance = await funcs.get_account_balance()
    price, project_id = payload.split('_')

    if int(price) <= client_balance:
        worker_chat = await users_db.get_chat_by_id(pchat_id)
        await funcs.start_project_update(
            project_id,
            int(price),
            user_id,
            worker_chat.user_id,
            chat_id,
            pchat_id,
        )
        await bot.send_message(pchat_id, b('Проект оплачен, приступайте к работе'))
        return b('Проект оплачен, уведомление отправлено автору')
    else:
        return b('У вас недостаточно средств, пополните баланс')


@dp.callback_query_handler(find_pair_chat,
                           text=TextQueries.REFUSE_WORK_PRICE,
                           pstatus=ProjectStatuses.ACTIVE,
                           user_role=UserRoles.client)
async def refuse_work_price(msg: types.Message, pchat_id: int):
    await msg.delete()
    await bot.send_message(pchat_id, b('Заказчик отказался от предложенной цены'))
