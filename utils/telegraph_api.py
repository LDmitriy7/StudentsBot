"""Модуль для создания и обновления личной страницы в telegraph."""
import asyncio
import atexit
from dataclasses import asdict
from typing import List

from telegraph import Telegraph

import datatypes
from config import TELEGRAPH_TOKEN
from texts import html_templates as templates

BASE_URL = 'https://telegra.ph/'

telegraph = Telegraph(TELEGRAPH_TOKEN)
atexit.register(asyncio.run, telegraph.close_session())


def _make_html_imgs(photo_urls: List[str]) -> str:
    """Создает html-текст c тегами <img/>."""
    photo_urls = ''.join([f'<img src="{url}"/>' for url in photo_urls])
    return photo_urls


def _make_html_reviews(reviews: List[datatypes.Review]) -> str:
    """Создает html-текст с отзывами по шаблону."""
    html_reviews = []
    for review in reviews:
        rating = asdict(review.rating)
        text_rating = {key: "⭐" * value for key, value in rating.items()}
        new_review = templates.REVIEW_TEMPLATE.format(
            client_name=review.client_name,
            text=review.text,
            **text_rating,
        )
        html_reviews.append(new_review)
    return '<hr/>'.join(html_reviews)


def _make_html_avg_rating(avg_rating: dict) -> str:
    """Создает html-текст со средним рейтингом по шаблону."""
    quality, contact, terms = avg_rating['quality'], avg_rating['contact'], avg_rating['terms']

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
        photo_urls: List[str], avg_rating: dict, reviews: List[datatypes.Review]) -> str:
    """Создает весь html-контент для личной страницы исполнителя."""
    content = templates.PAGE_TEMPLATE.format(
        deals_amount=deals_amount,
        biography=biography or '<b>Автор ничего не написал</b>',
        subjects=', '.join(subjects) or '<b>Не выбраны</b>',
        invite_project_url=invite_project_url,
        avg_rating=_make_html_avg_rating(avg_rating),
        images=_make_html_imgs(photo_urls),
        reviews=_make_html_reviews(reviews),
        reviews_amount=len(reviews),
    )
    return content


async def create_page(nickname: str, html_content: str, page_url: str = None) -> str:
    """Создает или редактирует [если задан page_url] страницу исполнителя. Возращает ссылку на нее."""
    request_data = {
        'title': f'Страница автора {nickname}',
        'author_name': 'Бот для студентов',
        'author_url': 'https://t.me/test2_test_bot',
        'html_content': html_content
    }

    if page_url:
        page_path = page_url.removeprefix(BASE_URL)
        response = await telegraph.edit_page(path=page_path, **request_data)
    else:
        response = await telegraph.create_page(**request_data)

    link = BASE_URL + response['path']
    return link
