from aiogram import types

from loader import dp
from texts.subjects import ALL_SUBJECTS


def find_subjects(query: types.InlineQuery):
    """Поиск подходящих предметов"""
    query = query.query.lower()
    subjects = {s for s in ALL_SUBJECTS if query in s.lower()}
    results = []

    for index, s in enumerate(subjects):
        if index > 19:
            break

        imc = types.InputMessageContent(message_text=s)
        result = types.InlineQueryResultArticle(
            id=str(index),
            title=s,
            input_message_content=imc,
        )
        results.append(result)
    return results


@dp.inline_handler(lambda query: query.query, state='*')
async def suggest_subjects(query: types.InlineQuery):
    await query.answer(results=find_subjects(query))
