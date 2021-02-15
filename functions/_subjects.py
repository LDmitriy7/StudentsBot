from aiogram import types

import subfuncs
from texts.subjects import ALL_SUBJECTS

__all__ = ['find_subjects']


def find_subjects(query: types.InlineQuery = None) -> list[types.InlineQueryResultArticle]:
    """Поиск предметов, содержащих текст запроса в названии.
    By default: query = current InlineQuery"""

    if query is None:
        query = types.InlineQuery.get_current()

    def make_result(subject: str, index: int):
        imc = types.InputMessageContent(message_text=subject)
        return types.InlineQueryResultArticle(
            id=str(index),
            title=subject,
            input_message_content=imc,
        )

    subjects = subfuncs.find_objects(query.query, ALL_SUBJECTS)
    return [make_result(r, i) for i, r in enumerate(subjects)]
