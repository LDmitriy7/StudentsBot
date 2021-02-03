from collections import namedtuple
from typing import List

from telegraph import Telegraph

from config import TELEGRAPH_TOKEN

Review = namedtuple('Review', ['client_name', 'rating', 'text'])

telegraph = Telegraph(TELEGRAPH_TOKEN)
BASE_URL = 'https://telegra.ph/'

PAGE_TEMPLATE = """
<p><b>Количество сделок 📝:</b> {deals_amount}</p>
<p><b>Предметы 📚:</b> {subjects}</p>
<p><b><a href="{offer_project_url}">Предложить автору проект 🤝</a></b>
(Нажмите на ссылку и вернитесь в бота)</p>

<p><b>Биография 👤:</b></p>
<blockquote>{biography}</blockquote>

<h3>Средний рейтинг 🌟:</h3>
{avg_rating}

<h3>Примеры работ 🎓:</h3>
<p>{images}</p>

<h3>Отзывы ({reviews_amount}):</h3>
{reviews}
"""

REVIEW_TEMPLATE = """
<aside>{client_name}:</aside>
<blockquote>{text}</blockquote>

<p>Качество: {quality}</p>
<p>Сроки: {terms}</p>
<p>Контактность: {contact}</p>
"""

AVG_RATING_TEMPLATE = """
<p>Качество: {quality} ({quality_num})</p>
<p>Сроки: {terms} ({terms_num})</p>
<p>Контактность: {contact} ({contact_num})</p>
"""


def _make_html_imgs(photo_urls: List[str]) -> str:
    """Создает текст c html-тегами <img/>."""
    photo_urls = ''.join([f'<img src="{url}"/>' for url in photo_urls])
    return photo_urls


def _make_html_reviews(reviews: List[Review]) -> str:
    """Создает текст с html-отзывами по шаблону."""
    html_reviews = []
    for review in reviews:
        rating = {key: "⭐" * value for key, value in review.rating.items()}
        new_review = REVIEW_TEMPLATE.format(
            client_name=review.client_name,
            text=review.text,
            **rating,
        )
        html_reviews.append(new_review)
    return '<hr/>'.join(html_reviews)


def _make_html_avg_rating(reviews: List[Review]) -> str:
    """Создает средний рейтинг по html-шаблону."""
    quality = 0
    contact = 0
    terms = 0
    for review in reviews:
        rates = review.rating
        quality += rates['quality']
        contact += rates['contact']
        terms += rates['terms']
    reviews_amount = len(reviews) or 1
    quality /= reviews_amount
    contact /= reviews_amount
    terms /= reviews_amount

    html_text = AVG_RATING_TEMPLATE.format(
        quality=round(quality) * "⭐",
        quality_num=f'{quality:.2f}',
        contact=round(contact) * "⭐",
        contact_num=f'{contact:.2f}',
        terms=round(terms) * "⭐",
        terms_num=f'{terms:.2f}',
    )
    return html_text


def make_html_content(
        deals_amount: int, biography: str, subjects: List[str], offer_project_url: str,
        photo_urls: List[str], reviews: List[Review]
):
    avg_rating = _make_html_avg_rating(reviews)
    subjects = ', '.join(subjects)
    html_imgs = _make_html_imgs(photo_urls)
    html_reviews = _make_html_reviews(reviews)

    biography = biography or '<b>Автор ничего не написал</b>'
    subjects = subjects or '<b>Не выбраны</b>'

    content = PAGE_TEMPLATE.format(
        deals_amount=deals_amount,
        biography=biography,
        subjects=subjects,
        offer_project_url=offer_project_url,
        avg_rating=avg_rating,
        images=html_imgs,
        reviews=html_reviews,
        reviews_amount=len(reviews)
    )
    return content


def create_page(nickname: str, html_content: str, page_url: str = None):
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


if __name__ == '__main__':
    offer_page_url = 'https://t.me/test2_test_bot?start=offer_project_724477101'
    html_content = make_html_content(0, 'Я python-программист', [], offer_page_url, [], [])
    print(create_page('Test3', html_content))
