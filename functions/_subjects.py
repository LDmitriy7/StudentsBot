from aiogram import types

import subfuncs
from subfuncs.currents2 import Currents
from texts.subjects import ALL_SUBJECTS

__all__ = ['find_subjects']


@Currents.set
async def find_subjects(*, iquery: types.InlineQuery) -> list[types.InlineQueryResultArticle]:
    """Поиск предметов, содержащих текст запроса в названии."""

    def make_result(index: int, subject: str):
        imc = types.InputMessageContent(message_text=subject)
        return types.InlineQueryResultArticle(
            id=str(index),
            title=subject,
            input_message_content=imc,
        )

    subjects = subfuncs.find_strings(iquery.query, ALL_SUBJECTS)
    return [make_result(i, s) for i, s in enumerate(subjects)]
