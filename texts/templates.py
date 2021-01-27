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

_BID_TEMPLATE = """
Автор <a href="{worker_url}">{worker_nickname}</a> откликнулся на ваш проект:

{bid_text}
"""


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


def form_bid_text(worker_nickname: str, worker_url: str, bid_text: str):
    text = _BID_TEMPLATE.format(
        worker_url=worker_url,
        worker_nickname=worker_nickname,
        bid_text=bid_text,
    )
    return text


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
    bid1 = form_bid_text('http://test.ru', 'Dimka5667', 'Текст заявки, не меньше 15 символов')

    print(post1)
    print(post2)
    print(bid1)
