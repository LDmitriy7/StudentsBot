from datatypes import PairChats
from loader import bot, users_db
from utils.chat_creator import create_pair_chats

__all__ = ['create_chats', 'get_chat_link']

GROUP_NUM = 0


async def create_chats(client_id: int, worker_id: int, project_id: str) -> PairChats:
    """Создает чаты с порядковым номером в названии и сохраняет их."""
    global GROUP_NUM
    GROUP_NUM += 1

    await bot.send_chat_action(client_id, 'typing')
    pair_chats = await create_pair_chats(f'Нора #{GROUP_NUM}', project_id, client_id, worker_id)
    client_chat, worker_chat = pair_chats.client_chat, pair_chats.worker_chat

    await users_db.add_chat(client_chat.id, client_chat)
    await users_db.add_chat(worker_chat.id, worker_chat)
    return pair_chats


def get_chat_link(chat_id: int) -> str:
    chat = users_db.get_chat_by_id(chat_id)
    return chat.link
