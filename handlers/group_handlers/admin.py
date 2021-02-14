from aiogram import types

from config import GROUP_ADMIN_ID
from filters import find_pair_chat
from keyboards.inline_funcs import GroupMenuKeyboard
from loader import dp, users_db, bot


@dp.callback_query_handler(find_pair_chat, text=GroupMenuKeyboard.CALL_ADMIN)
async def call_admin(query: types.CallbackQuery, pchat_id: int):
    chat = await users_db.get_chat_by_id(query.message.chat.id)
    await bot.send_message(GROUP_ADMIN_ID, f'Вас вызывают в чат: {chat.link}')
    await query.answer('Вы вызвали администратора, ожидайте...', show_alert=True)
    await bot.send_message(pchat_id, '<b>Ваш собеседник вызвал администратора.</b>')
