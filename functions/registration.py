from loader import users_db


async def get_all_nicknames() -> set:
    """Возращает сет всех никнеймов пользователей."""
    all_nicknames = set()
    for account in await users_db.get_all_accounts():
        profile = account.get('profile')
        if profile:
            nickname = profile['nickname']
            all_nicknames.add(nickname)
    return all_nicknames
