from aiogram import types
from loader import bot
from data_types.for_quests import Quest, QuestText, QuestFunc

__all__ = ['ask_question']


async def ask_question(question: list[Quest]):
    chat = types.Chat.get_current()

    for item in question:
        if isinstance(item, QuestText):
            await bot.send_message(chat.id, item.text, reply_markup=item.keyboard)
        elif isinstance(item, QuestFunc):
            await item.async_func()
