from aiogram import types
from aiogram.dispatcher.currents import CurrentObjects
import subfuncs

from texts.subjects import ALL_SUBJECTS

__all__ = ['find_subjects']


@CurrentObjects.decorate
async def find_subjects(*, idata) -> list[types.InlineQueryResultArticle]:
    """Поиск предметов, содержащих текст запроса в названии."""

    def make_result(index: int, subject: str):
        imc = types.InputMessageContent(message_text=subject)
        return types.InlineQueryResultArticle(
            id=str(index),
            title=subject,
            input_message_content=imc,
        )

    subjects = subfuncs.find_strings(idata, ALL_SUBJECTS)
    return [make_result(i, s) for i, s in enumerate(subjects)]
