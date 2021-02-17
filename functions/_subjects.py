from aiogram import types

import subfuncs
from texts.subjects import ALL_SUBJECTS
from subfuncs import decorators as current

__all__ = ['find_subjects']


@current.set_query
def find_subjects(query: types.InlineQuery = None) -> list[types.InlineQueryResultArticle]:
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
