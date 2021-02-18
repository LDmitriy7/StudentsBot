from data_types import data_classes
from loader import users_db, dp
from subfuncs import decorators as current
from aiogram import types

__all__ = ['save_bid', 'save_profile']


async def save_bid(client_id: int, project_id: str, worker_id: int, text: str) -> str:
    bid = data_classes.Bid.from_dict(locals())
    bid_id = await users_db.add_bid(bid)  # сохранение заявки
    return bid_id


@current.set_user
async def save_profile(user: types.User = None, **kwargs) -> data_classes.Profile:
    profile_data = await dp.current_state().get_data()
    profile_data = dict(**profile_data, **kwargs)
    profile = data_classes.Profile.from_dict(profile_data)
    await users_db.update_account_profile(user.id, profile)
    return profile
