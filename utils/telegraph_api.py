from typing import List

from telegraph import Telegraph
from texts import html_templates as templates
from config import TELEGRAPH_TOKEN
from functions.reviews import count_avg_rating
import atexit
import asyncio

telegraph = Telegraph(TELEGRAPH_TOKEN)
atexit.register(asyncio.run, telegraph.close_session())

BASE_URL = 'https://telegra.ph/'


def _make_html_imgs(photo_urls: List[str]) -> str:
    """Создает html-текст c тегами <img/>."""
    photo_urls = ''.join([f'<img src="{url}"/>' for url in photo_urls])
    return photo_urls


def _make_html_reviews(reviews: List[dict]) -> str:
    """Создает html-текст с отзывами по шаблону."""
    html_reviews = []
    for review in reviews:
        rating = {key: "⭐" * value for key, value in review['rating'].items()}
        new_review = templates.REVIEW_TEMPLATE.format(
            client_name=review['client_name'],
            text=review['text'],
            **rating,
        )
        html_reviews.append(new_review)
    return '<hr/>'.join(html_reviews)


def _make_html_avg_rating(reviews: List[dict]) -> str:
    """Создает html-текст со средним рейтингом по шаблону."""
    rating = count_avg_rating(reviews)
    quality, contact, terms = rating['quality'], rating['contact'], rating['terms']

    html_text = templates.AVG_RATING_TEMPLATE.format(
        quality=round(quality) * "⭐",
        quality_num=quality,
        contact=round(contact) * "⭐",
        contact_num=contact,
        terms=round(terms) * "⭐",
        terms_num=terms,
    )
    return html_text


def make_html_content(
        deals_amount: int, biography: str, subjects: List[str], invite_project_url: str,
        photo_urls: List[str], reviews: List[dict]) -> str:
    """Создает весь html-контент для личной страницы исполнителя."""
    content = templates.PAGE_TEMPLATE.format(
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


async def create_page(nickname: str, html_content: str, page_url: str = None) -> str:
    """Создает или редактирует [если задан page_url] страницу исполнителя. Возращает ссылку."""
    request_data = {
        'title': f'Страница автора {nickname}',
        'author_name': 'Бот для студентов',
        'author_url': 'https://t.me/test2_test_bot',
        'html_content': html_content
    }

    if page_url:
        page_path = page_url.replace(BASE_URL, '')
        response = await telegraph.edit_page(path=page_path, **request_data)
    else:
        response = await telegraph.create_page(**request_data)

    link = BASE_URL + response['path']
    return link
