"""All classes for making questions."""

from typing import List

from aiogram import types

from _qustions import Quest, QuestText, QuestFunc


async def ask_question(msg: types.Message, question: List[Quest]):
    for item in question:
        if isinstance(item, QuestText):
            await msg.answer(item.text, reply_markup=item.keyboard)
        elif isinstance(item, QuestFunc):
            await item.async_func(msg)
