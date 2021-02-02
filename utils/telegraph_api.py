from telegraph import Telegraph
import asyncio
from typing import List
from collections import namedtuple

access_token = 'be3cb0f4c945f16ca942bec2a979625bcea94e4b342fe639ed7ba7607397'
telegraph = Telegraph(access_token)

BASE_URL = 'https://telegra.ph/'
Review = namedtuple('Review', ['client_name', 'rating', 'text'])

page_template = """
<p><b>Количество сделок 📝:</b> {deals_amount}</p>
<p><b>Предметы 📚:</b> {subjects}</p>

<h4>Биография 👤:</h4>
<blockquote>{biography}</blockquote>

<h4><b>Средний рейтинг 🌟:</b></h4>
<p>{avg_rating}</p>

<h4>Примеры работ:</h4>
{html_imgs}

<h3>Отзывы:</h3>
{reviews}
"""

review_template = """
<aside><b>{client_name}:</b></aside>
<blockquote>{text}</blockquote>

<p>Качество: {quality}</p>
<p>Сроки: {terms}</p>
<p>Контактность: {contact}</p>
"""


def make_html_imgs(photo_urls: List[str]) -> str:
    """Создает текст c html-тегами <img/>."""
    photo_urls = ''.join([f'<img src="{url}"/>' for url in photo_urls])
    return photo_urls


def make_html_reviews(reviews: List[Review]) -> str:
    """Создает текст с html-отзывами по шаблону."""
    html_reviews = []
    for review in reviews:
        rating = {key: "⭐" * value for key, value in review.rating.items()}
        new_review = review_template.format(
            client_name=review.client_name,
            text=review.text,
            **rating,
        )
        html_reviews.append(new_review)
    return '<hr/>'.join(html_reviews)


review1 = Review(
    'Арсений Акопов',
    {'quality': 4, 'contact': 5, 'terms': 4},
    'Спасибо, все выполнил качественно, буду обращаться еще'
)


def make_html_content(deals_amount: int, biography: str, subjects: List[str], works: List[str], reviews: List[Review]):
    avg_rating = 'test'
    subjects = ', '.join(subjects)
    html_imgs = make_html_imgs(works)
    reviews = make_html_reviews(reviews)

    content = page_template.format(
        deals_amount=deals_amount,
        biography=biography,
        subjects=subjects,
        avg_rating=avg_rating,
        html_imgs=html_imgs,
        reviews=reviews,
    )
    return content


# никнейм, биография, предметы, примеры работ, ссылка на персональный проект, отзывы + количество сделок
async def create_page(nickname: str, html_content: str, page_url: str = None):
    request_data = {
        'title': f'Страница автора {nickname}',
        'author_name': 'Бот для студентов',
        'author_url': 'https://t.me/test2_test_bot',
        'html_content': html_content
    }

    if page_url:
        page_path = page_url.replace(BASE_URL, '')
        response = telegraph.edit_page(path=page_path, **request_data)
    else:
        response = telegraph.create_page(**request_data)

    link = BASE_URL + response['path']
    return link


files = [
    'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Disambig.svg/30px-Disambig.svg.png',
    'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Disambig.svg/30px-Disambig.svg.png',
]

page_url = 'Stranica-avtora-Dimka34-02-02-4'
html_content = make_html_content(
    45, 'Я python-программист, пишу ботов и парсеры больше 2 лет',
    ['Математика', 'Русский язык', 'Общая физика', 'Украинский язык'],
    files, [review1, review1]
)

c = create_page('Dimka34', html_content, page_url=page_url)
r = asyncio.run(c)
print(r)
