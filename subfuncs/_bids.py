from database_api import MongoDB
from texts import templates

__all__ = ['get_worker_bid_text']


async def get_worker_bid_text(db: MongoDB, avg_rating: dict,
                              worker_id: int, project_id: str, bid_text: str) -> str:
    """Формирует полный текст для заявки исполнителя на проект."""
    account = await db.get_account_by_id(worker_id)
    project = await db.get_project_by_id(project_id)

    avg_rating_text = templates.form_avg_rating_text(avg_rating)

    return templates.form_worker_bid_text(
        account.profile.nickname, account.page_url, project.post_url, avg_rating_text, bid_text
    )
