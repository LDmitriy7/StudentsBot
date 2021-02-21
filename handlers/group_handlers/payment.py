from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.utils.markdown import hbold as b

import functions as funcs
from data_types import ProjectStatuses, UserRoles, Prefixes, TextQueries
from filters import find_pair_chat, QueryPrefix
from keyboards import inline_funcs
from keyboards.inline_funcs import GroupMenuKeyboard
from loader import dp, users_db, bot
from questions import ForGroups as States


@dp.callback_query_handler(find_pair_chat,
                           text=GroupMenuKeyboard.OFFER_PRICE,
                           pstatus=ProjectStatuses.ACTIVE,
                           user_role=UserRoles.WORKER)
async def ask_work_price(query: types.CallbackQuery):
    return UpdateData(new_state=States.ask_work_price)


@dp.message_handler(find_pair_chat,
                    state=States.ask_work_price,
                    pstatus=ProjectStatuses.ACTIVE,
                    user_role=UserRoles.WORKER)
async def offer_price(msg: types.Message, pchat_id: int):
    if not msg.text.isdigit():
        return 'Ошибка, отправьте число'

    price = int(msg.text)
    chat = await users_db.get_chat_by_id(msg.chat.id)
    client_text = f'Автор предлагает вам сделку за <b>{price} грн</b>'
    keyboard = inline_funcs.pay_for_project(price, chat.project_id)
    await bot.send_message(pchat_id, client_text, reply_markup=keyboard)
    return UpdateData(on_conv_exit='Заявка отправлена, мы пришлем вам уведомление в случае оплаты.')


@dp.callback_query_handler(find_pair_chat,
                           QueryPrefix(Prefixes.PAY_FOR_PROJECT_),
                           pstatus=ProjectStatuses.ACTIVE,
                           user_role=UserRoles.CLIENT)
async def pay_for_project(query: types.CallbackQuery, pchat_id: int, payload: str):
    client_balance = await funcs.get_account_balance()
    price, project_id = payload.split('_')

    if int(price) <= client_balance:
        worker_chat = await users_db.get_chat_by_id(pchat_id)
        await funcs.start_project_update(
            project_id,
            int(price),
            query.from_user.id,
            worker_chat.user_id,
            query.message.chat.id,
            pchat_id,
        )
        await bot.send_message(pchat_id, b('Проект оплачен, приступайте к работе'))
        return b('Проект оплачен, уведомление отправлено автору')
    else:
        return b('У вас недостаточно средств, пополните баланс')


@dp.callback_query_handler(find_pair_chat,
                           text=TextQueries.REFUSE_WORK_PRICE,
                           pstatus=ProjectStatuses.ACTIVE,
                           user_role=UserRoles.CLIENT)
async def refuse_work_price(query: types.CallbackQuery, pchat_id: int):
    await query.message.delete()
    await bot.send_message(pchat_id, b('Заказчик отказался от предложенной цены'))
