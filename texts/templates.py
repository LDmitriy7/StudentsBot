"""Содержит функции для формирования текстов по шаблонам."""

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
Качество: {quality} ({quality_num})
Сроки: {terms} ({terms_num})
Контактность: {contact} ({contact_num})\
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
    return _CLIENT_BID_TEMPLATE.format(client_name=client_name)


def form_avg_rating_text(rating: dict) -> str:
    """Создает текст со средним рейтингом по шаблону."""
    quality, contact, terms = rating['quality'], rating['contact'], rating['terms']

    return _AVG_RATING_TEMPLATE.format(
        quality=round(quality) * "⭐",
        quality_num=quality,
        contact=round(contact) * "⭐",
        contact_num=contact,
        terms=round(terms) * "⭐",
        terms_num=terms,
    )


def form_subjects_text(subjects: list) -> str:
    title = '<b>Ваши предметы:</b>'
    subjects = [f' • {s}' for s in subjects]
    result = title + '\n' + '\n'.join(subjects)
    return result


def form_post_text(status: str, post_data: dict, with_note=False):
    """Requires all fields from project.data"""
    post_data = post_data.copy()

    subject = post_data['subject'].replace(' ', '_')
    work_type = post_data['work_type'].replace(' ', '_')

    price = post_data['price']
    price = f'{price} грн' if price else 'Договорная'

    date = post_data['date'].split('-')
    date = f'{date[2]}.{date[1]}'

    emojis = {'Активен': '🔥', 'Выполняется': '⏳', 'Выполнен': '✅'}
    status = f'{emojis[status]} {status}'

    note = post_data['note']
    note = f'<b>Ваша заметка:</b> {note}' if note and with_note else ''

    post_data.update(
        subject=subject,
        work_type=work_type,
        price=price,
        date=date,
        status=status,
        note=note,
    )
    text = _POST_TEMPLATE.format(**post_data)
    return text


def form_worker_bid_text(worker_nickname: str, worker_url: str, post_url: str, avg_rating: str, bid_text: str) -> str:
    text = _WORKER_BID_TEMPLATE.format(
        worker_url=worker_url,
        worker_nickname=worker_nickname,
        post_url=post_url,
        avg_rating=avg_rating,
        bid_text=bid_text,
    )
    return text


def form_profile_template(nickname: str, phone_number: str, email: str, page_url: str):
    return _PROFILE_TEMPLATE.format(
        nickname=nickname,
        phone_number=phone_number,
        email=email,
        page_url=page_url,
    )


if __name__ == '__main__':
    status1 = 'Выполняется'
    post_data1 = dict(
        subject='Общая физика',
        work_type='Онлайн помощь',
        date='2021-01-27',
        price=None,
        note=None,
        description='Тестирование. Описание проекта, минимум в 15 символов.'
    )
    status2 = 'Активен'
    post_data2 = dict(
        subject='Математика',
        work_type='Практика',
        date='2016-09-30',
        price=300,
        note='Покормить кота',
        description='Тестирование. Описание проекта, минимум в 15 символов.'
    )

    post1 = form_post_text(status1, post_data1)
    post2 = form_post_text(status2, post_data2, with_note=True)
    bid1 = form_worker_bid_text('http://test.ru', 'Dimka5667', 'Текст заявки, не меньше 15 символов')

    print(post1)
    print(post2)
    print(bid1)
