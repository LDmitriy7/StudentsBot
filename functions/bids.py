from aiogram.dispatcher import FSMContext
from loader import users_db


async def get_full_bid(state: FSMContext):
    """Return bid_data, worker_name, post_url, note."""
    udata = await state.get_data()

    project_id = udata['project_id']
    project = await users_db.get_project_by_id(project_id)

    post_url = project['post_url']
    note = project['data']['note']
    worker_name = udata['worker_name']

    bid_data = dict(user_id=project['user_id'], worker_id=udata['worker_id'], project_id=project_id)
    return bid_data, worker_name, post_url, note
