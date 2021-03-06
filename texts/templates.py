"""Содержит функции для формирования текстов по шаблонам."""

from copy import deepcopy
from dataclasses import asdict

from data_types import data_models

_POST_TEMPLATE = """
<b>{status}</b>

#{work_type}
#{subject}

{description}

<b>Сдача:</b> {date}
<b>Цена:</b> {price}
{note}
"""

_AVG_RATING_TEMPLATE = """\
Качество: {quality_text} ({quality:.2f})
Сроки: {terms_text} ({terms:.2f})
Контактность: {contact_text} ({contact:.2f})\
"""

_WORKER_BID_TEMPLATE = """
<a href="{post_url}">&#8203;</a>\
Автор <a href="{worker_url}">{worker_nickname}</a> отклинкулся на ваш проект:

<b>Средний рейтинг</b>:
{avg_rating}

<b>Комментарий</b>:
{bid_text}
"""

_CLIENT_BID_TEMPLATE = """
Заказчик {client_name} предлагает вам персональный проект
"""

_PROFILE_TEMPLATE = """
Никнейм: {nickname}
Телефон: {phone_number}
Email: {email}

Ссылка на личную страницу:
{page_url}
"""


def form_client_bid_text(client_name: str) -> str:
    """Создает текст для заявки исполнителю от клиента."""
    return _CLIENT_BID_TEMPLATE.format(**locals())


def form_avg_rating_text(rating: dict) -> str:
    """Создает текст со средним рейтингом по шаблону."""
    text_rating = {f'{rate}_text': round(amount) * '⭐' for rate, amount in rating.items()}
    return _AVG_RATING_TEMPLATE.format(**rating, **text_rating)


def form_subjects_text(subjects: list) -> str:
    """Создает список предметов (текст)."""
    title = '<b>Ваши предметы:</b>'
    subjects = [f' • {s}' for s in subjects]
    result = title + '\n' + '\n'.join(subjects)
    return result


def form_post_text(status: str, post_data: data_models.ProjectData, with_note=False) -> str:
    """Form text for post for channel."""
    post_data = deepcopy(post_data)

    emojis = {'Активен': '🔥', 'Выполняется': '⏳', 'Выполнен': '✅', 'Оставлен отзыв': '✅'}
    status = f'{emojis.get(status, "")} {status}'

    post_data.subject = post_data.subject.replace(' ', '_')
    post_data.work_type = post_data.work_type.replace(' ', '_')

    price = post_data.price
    post_data.price = f'{price} грн' if price else 'Договорная'

    date = post_data.date.split('-')
    post_data.date = f'{date[2]}.{date[1]}'

    note = post_data.note
    post_data.note = f'<b>Ваша заметка:</b> {note}' if note and with_note else ''

    return _POST_TEMPLATE.format(**asdict(post_data), status=status)


def form_worker_bid_text(worker_nickname: str, worker_url: str, post_url: str, avg_rating: str, bid_text: str) -> str:
    return _WORKER_BID_TEMPLATE.format(**locals())


def form_profile_template(nickname: str, phone_number: str, email: str, page_url: str):
    return _PROFILE_TEMPLATE.format(**locals())
