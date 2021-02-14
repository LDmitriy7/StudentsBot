from aiogram import types
from aiogram.dispatcher import FSMContext

import functions as funcs
from datatypes import ProjectStatuses, UserRoles, Prefixes
from filters import find_pair_chat, QueryPrefix
from keyboards import inline_funcs
from keyboards.inline_funcs import GroupMenuKeyboard
from loader import dp, users_db, bot
from states import Payment as States


@dp.callback_query_handler(
    find_pair_chat, text=GroupMenuKeyboard.OFFER_PRICE,
    pstatus=ProjectStatuses.ACTIVE, user_role=UserRoles.WORKER
)
async def ask_work_price(query: types.CallbackQuery):
    await States.ask_work_price.set()
    await query.message.answer('Введите цену в гривнах:')


@dp.message_handler(
    find_pair_chat, state=States.ask_work_price,
    pstatus=ProjectStatuses.ACTIVE, user_role=UserRoles.WORKER
)
async def offer_price(msg: types.Message, pchat_id: int, state: FSMContext):
    if msg.text.isdigit():
        price = int(msg.text)
        chat = await users_db.get_chat_by_id(msg.chat.id)
        client_text = f'Автор предлагает вам сделку за <b>{price} грн</b>'
        worker_text = 'Заявка отправлена, мы пришлем вам уведомление в случае оплаты.'
        keyboard = inline_funcs.pay_for_project(price, chat.project_id)
        await bot.send_message(pchat_id, client_text, reply_markup=keyboard)
        await msg.answer(worker_text)
        await state.finish()
    else:
        await msg.answer('Ошибка, отправьте число')


@dp.callback_query_handler(
    find_pair_chat, QueryPrefix(Prefixes.PAY_FOR_PROJECT_),
    pstatus=ProjectStatuses.ACTIVE, user_role=UserRoles.CLIENT
)
async def pay_for_project(query: types.CallbackQuery, pchat_id: int, payload: str):
    client_id, msg = query.from_user.id, query.message
    client_balance = await funcs.get_account_balance(client_id)
    price, project_id = payload.split('_')
    price = int(price)

    if price <= client_balance:
        worker_chat = await users_db.get_chat_by_id(pchat_id)
        await funcs.start_project_update(
            project_id, price, client_id, worker_chat.user_id, msg.chat.id, pchat_id
        )
        await bot.send_message(pchat_id, '<b>Проект оплачен, приступайте к работе</b>')
        await msg.answer('<b>Проект оплачен, уведомление отправлено автору</b>')
    else:
        await msg.answer('У вас недостаточно средств, пополните баланс')


@dp.callback_query_handler(
    find_pair_chat, text=inline_funcs.REFUSE_WORK_PRICE,
    pstatus=ProjectStatuses.ACTIVE, user_role=UserRoles.CLIENT
)
async def refuse_work_price(query: types.CallbackQuery, pchat_id: int):
    await query.message.delete()
    await bot.send_message(pchat_id, 'Заказчик отказался от предложенной цены')
