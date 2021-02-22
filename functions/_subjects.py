from aiogram import types

import subfuncs
from texts.subjects import ALL_SUBJECTS
from aiogram.contrib.currents import SetCurrent

__all__ = ['find_subjects']


@SetCurrent.inline_query
async def find_subjects(*, query: types.InlineQuery) -> list[types.InlineQueryResultArticle]:
    """Поиск предметов, содержащих текст запроса в названии."""

    def make_result(index: int, subject: str):
        imc = types.InputMessageContent(message_text=subject)
        return types.InlineQueryResultArticle(
            id=str(index),
            title=subject,
            input_message_content=imc,
        )

    subjects = subfuncs.find_strings(query.query, ALL_SUBJECTS)
    return [make_result(i, s) for i, s in enumerate(subjects)]
