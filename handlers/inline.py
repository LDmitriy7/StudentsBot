from aiogram import types

from loader import dp
from texts import subjects


def get_subjects(query: types.InlineQuery):
    """Поиск подходящих предметов"""
    query = query.query.lower()
    SUBJECTS = {s for s in subjects.SUBJECTS if query in s.lower()}
    results = []
    for index, s in enumerate(SUBJECTS):
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


# TODO: ограничить состояния?
@dp.inline_handler(lambda query: query.query, state='*')
async def suggest_subjects(query: types.InlineQuery):
    await query.answer(results=get_subjects(query))
