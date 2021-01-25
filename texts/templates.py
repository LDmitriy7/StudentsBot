POST_TEMPLATE = """
<b>{status}</b>

#{work_type}
#{subject}
<a href="{media_url}">&#4448;</a>
{description}

<b>Сдача:</b> {date}
<b>Цена:</b> {price}
"""

BID_TEMPLATE = """
Автор <a href="{worker_url}"{worker_nickname}</a> откликнулся на ваш <a href="{post_url}">проект</a>:

{bid_text}
————————————————————
<i>Ваша заметка к проекту</i>:
{note}
"""


def form_post_text(post_data: dict, with_note=False):
    post_data = post_data.copy()

    subject = post_data['subject'].replace(' ', '_')
    work_type = post_data['work_type'].replace(' ', '_')

    price = post_data.get('price')
    price = f'{price} грн' if price else 'Договорная'

    date = post_data['date'].split('-')
    date = f'{date[2]}.{date[1]}'

    status = post_data['status']
    emojis = {'Активен': '🔥', 'Выполняется': '⏳', 'Выполнен': '✅'}
    status = f'{emojis[status]} {status}'

    post_data.update(subject=subject, work_type=work_type, price=price, date=date, status=status)
    text = POST_TEMPLATE.format(**post_data)

    if with_note:
        note = post_data.get('note')
        note = f'<b>Ваша заметка:</b> {note}' if note else ''  # TODO: заметка = None при пропуске
        text += note

    return text


if __name__ == '__main__':
    post_data1 = dict(
        subject='Общая физика',
        work_type='Онлайн помощь',
        date='2021-01-27',
        note=None,
        status='Выполняется',
        media_url='https://telegram.org/',
        description='Тестирование. Описание проекта, минимум в 15 символов.'
    )

    post_data2 = dict(
        subject='Математика',
        work_type='Практика',
        date='2016-09-30',
        price=300,
        note='Покормить кота',
        status='Активен',
        media_url='https://telegram.org/',
        description='Тестирование. Описание проекта, минимум в 15 символов.'
    )
    post1 = form_post_text(post_data1)
    post2 = form_post_text(post_data2, with_note=True)

    print(post1)
    print(post2)
