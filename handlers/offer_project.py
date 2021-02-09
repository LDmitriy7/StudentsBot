from loader import dp, users_db, bot
from aiogram import types
from keyboards import inline_funcs, markup
from keyboards.inline_funcs import Prefixes
from filters import InlinePrefix, QueryPrefix
from utils.chat_creator import create_pair_chats
from type_classes import Chat


@dp.inline_handler(InlinePrefix(Prefixes.OFFER_PROJECT_))
async def send_offer_to_worker(query: types.InlineQuery, payload: str):
    text = 'Предлагаю вам персональный проект'
    keyboard = inline_funcs.pick_project(payload)
    imc = types.InputMessageContent(message_text=text)

    result = types.InlineQueryResultArticle(
        id='0',
        title='Предложить проект',
        description='Нажмите, чтобы предложить личный проект вашему собеседнику',
        input_message_content=imc,
        reply_markup=keyboard,
    )
    await query.answer([result], cache_time=0, is_personal=True)


@dp.callback_query_handler(QueryPrefix(Prefixes.PICK_PROJECT_), state='*')
async def pick_project(query: types.CallbackQuery, payload: str):
    project = await users_db.get_project_by_id_test(payload)
    client_id = project.client_id
    worker_id = query.from_user.id

    if worker_id == client_id:
        await query.answer('Вы не можете сами принять проект')
        return

    account = await users_db.get_account_by_id_test(worker_id)
    if not (account and account.profile):
        await query.answer('Сначала пройдите регистрацию в боте', markup.main_kb)
        await bot.send_message(worker_id, 'Загляните в меню исполнителя')
        return

    chats = await create_pair_chats('Нора3', payload, client_id, worker_id)

    async def send_invite_msg(user_id: int, chat: Chat):
        text = 'Ссылка в чат для принятого проекта'
        keyboard = inline_funcs.link_button('Перейти в чат', chat.link)
        await users_db.add_chat_test(chat)  # сохранение чата
        await bot.send_message(user_id, text, reply_markup=keyboard)

    await send_invite_msg(client_id, chats.client_chat)
    await send_invite_msg(worker_id, chats.worker_chat)

    new_text = '<b>Проект принят, ссылки в чат отправлены</b>'
    await bot.edit_message_text(new_text, inline_message_id=query.inline_message_id)
