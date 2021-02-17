from data_types import data_classes
from loader import users_db

__all__ = ['save_bid']


async def save_bid(client_id: int, project_id: str, worker_id: int, text: str) -> str:
    bid = data_classes.Bid.from_dict(locals())
    bid_id = await users_db.add_bid(bid)  # сохранение заявки
    return bid_id
