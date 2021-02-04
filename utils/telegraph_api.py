from collections import namedtuple
from typing import List

from telegraph import Telegraph

from config import TELEGRAPH_TOKEN

telegraph = Telegraph(TELEGRAPH_TOKEN)
BASE_URL = 'https://telegra.ph/'

_PAGE_TEMPLATE = """
<p><b><a href="{invite_project_url}">Предложить автору проект 🤝</a></b></p>
<p><b>Количество сделок 📝:</b> {deals_amount}</p>
<p><b>Предметы 📚:</b> {subjects}</p>

<p><b>Биография 👤:</b></p>
<blockquote>{biography}</blockquote>

<h3>Средний рейтинг 🌟:</h3>
{avg_rating}

<h3>Примеры работ 🎓:</h3>
<p>{images}</p>

<h3>Отзывы ({reviews_amount}):</h3>
{reviews}
"""

_REVIEW_TEMPLATE = """
<aside>{client_name}:</aside>
<blockquote>{text}</blockquote>

<p>Качество: {quality}</p>
<p>Сроки: {terms}</p>
<p>Контактность: {contact}</p>
"""

_AVG_RATING_TEMPLATE = """
<p>Качество: {quality} ({quality_num})</p>
<p>Сроки: {terms} ({terms_num})</p>
<p>Контактность: {contact} ({contact_num})</p>
"""


def _make_html_imgs(photo_urls: List[str]) -> str:
    """Создает html-текст c тегами <img/>."""
    photo_urls = ''.join([f'<img src="{url}"/>' for url in photo_urls])
    return photo_urls


def _make_html_reviews(reviews: List[dict]) -> str:
    """Создает html-текст с отзывами по шаблону."""
    html_reviews = []
    for review in reviews:
        rating = {key: "⭐" * value for key, value in review['rating'].items()}
        new_review = _REVIEW_TEMPLATE.format(
            client_name=review['client_name'],
            text=review['text'],
            **rating,
        )
        html_reviews.append(new_review)
    return '<hr/>'.join(html_reviews)


def _make_html_avg_rating(reviews: List[dict]) -> str:
    """Создает html-текст со средним рейтингом по шаблону."""
    quality = 0
    contact = 0
    terms = 0
    for review in reviews:
        rating = review['rating']
        quality += rating['quality']
        contact += rating['contact']
        terms += rating['terms']

    reviews_amount = len(reviews) or 1
    quality /= reviews_amount
    contact /= reviews_amount
    terms /= reviews_amount

    html_text = _AVG_RATING_TEMPLATE.format(
        quality=round(quality) * "⭐",
        quality_num=f'{quality:.2f}',
        contact=round(contact) * "⭐",
        contact_num=f'{contact:.2f}',
        terms=round(terms) * "⭐",
        terms_num=f'{terms:.2f}',
    )
    return html_text


def make_html_content(
        deals_amount: int, biography: str, subjects: List[str], invite_project_url: str,
        photo_urls: List[str], reviews: List[dict]) -> str:
    """Создает весь html-контент для личной страницы исполнителя."""
    content = _PAGE_TEMPLATE.format(
        deals_amount=deals_amount,
        biography=biography or '<b>Автор ничего не написал</b>',
        subjects=', '.join(subjects) or '<b>Не выбраны</b>',
        invite_project_url=invite_project_url,
        avg_rating=_make_html_avg_rating(reviews),
        images=_make_html_imgs(photo_urls),
        reviews=_make_html_reviews(reviews),
        reviews_amount=len(reviews),
    )
    return content


def create_page(nickname: str, html_content: str, page_url: str = None) -> str:
    """Создает или редактирует [если задан page_url] страницу исполнителя. Возращает ссылку."""
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
