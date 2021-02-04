from aiogram import types


async def remove_button(query: types.CallbackQuery, index: int):
    """Remove one button from linked inline keyboard."""
    msg = query.message
    reply_markup = msg.reply_markup
    reply_markup.inline_keyboard.pop(index)
    await msg.edit_reply_markup(reply_markup)
