"""Модуль для создания и обновления личной страницы в telegraph."""
import asyncio
import atexit
from dataclasses import asdict

from aiograph import Telegraph

from config import TELEGRAPH_TOKEN, BOT_USERNAME
from data_types import data_models
from texts import html_templates as templates

BASE_URL = 'https://telegra.ph/'

telegraph = Telegraph(TELEGRAPH_TOKEN)
atexit.register(asyncio.run, telegraph.close())


async def _make_html_imgs(photo_urls: list[str]) -> str:
    """Создает html-текст c тегами <img/>."""

    async def make_img(photo_url: str):
        new_url = await telegraph.upload_from_url(photo_url)
        return f'<img src="{new_url}"/>'

    photo_urls = ''.join([await make_img(url) for url in photo_urls])
    return photo_urls


def _make_html_reviews(reviews: list[data_models.Review]) -> str:
    """Создает html-текст с отзывами по шаблону."""

    def make_review(review: data_models.Review) -> str:
        rating = asdict(review.rating)
        text_rating = {key: "⭐" * value for key, value in rating.items()}
        return templates.REVIEW_TEMPLATE.format(
            client_name=review.client_name,
            text=review.text,
            subject=review.subject,
            **text_rating,
        )

    return '<hr/>'.join(make_review(r) for r in reviews)


def _make_html_avg_rating(avg_rating: dict) -> str:
    """Создает html-текст со средним рейтингом по шаблону."""
    rates = {rate: round(amount) * "⭐" for rate, amount in avg_rating.items()}
    rates_num = {f'{rate}_num': amount for rate, amount in avg_rating.items()}
    return templates.AVG_RATING_TEMPLATE.format(**rates, **rates_num)


async def make_html_content(
        deals_amount: int, biography: str, subjects: list[str], invite_project_url: str,
        photo_urls: list[str], avg_rating: dict, reviews: list[data_models.Review]) -> str:
    """Создает весь html-контент для личной страницы исполнителя."""
    return templates.PAGE_TEMPLATE.format(
        deals_amount=deals_amount,
        biography=biography or '<b>Автор ничего не написал</b>',
        subjects=', '.join(subjects) or '<b>Не выбраны</b>',
        invite_project_url=invite_project_url,
        avg_rating=_make_html_avg_rating(avg_rating),
        images=await _make_html_imgs(photo_urls) or '<b>Нет примеров работ</b>',
        reviews=_make_html_reviews(reviews) or '<b>Пока нет отзывов</b>',
        reviews_amount=len(reviews),
    )


async def create_page(nickname: str, html_content: str, page_url: str = None) -> str:
    """Создает или редактирует [если задан page_url] страницу исполнителя. Возращает ссылку на нее."""
    title = f'Страница автора {nickname}'
    author_name = 'Бот для студентов'
    author_url = f'https://t.me/{BOT_USERNAME}'

    if page_url:
        page_path = page_url.removeprefix(BASE_URL)
        response = await telegraph.edit_page(page_path, title, html_content, author_name, author_url)
    else:
        response = await telegraph.create_page(title, html_content, author_name, author_url)

    print(html_content)
    return BASE_URL + response.path
