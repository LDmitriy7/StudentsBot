import datatypes

from texts.templates import form_avg_rating_text, form_post_text, form_worker_bid_text

# from texts.templates import form_client_bid_text, form_subjects_text

if __name__ == '__main__':
    status1 = 'Выполняется'
    post_data1 = datatypes.ProjectData(
        'Онлайн помощь',
        'Общая физика',
        '2021-01-27',
        'Тестирование. Описание проекта, минимум в 15 символов.',
        456,
        'Покормить кота'
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

    print(form_avg_rating_text({'quality': 3.5664, 'contact': 5, 'terms': 4.5}))

    post1 = form_post_text(status1, post_data1, with_note=True)
    # post2 = form_post_text(status2, post_data2, with_note=True)
    bid1 = form_worker_bid_text('Dimka5667', 'http://test.ru', 'http://test2.ru', 'Рейтинг',
                                'Текст заявки, не меньше 15 символов')

    print(post1)
    # print(post2)
    # print(bid1)
