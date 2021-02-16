from loader import dp

__all__ = ['update_user_data']


async def update_user_data(new_data: dict):
    """Set, delete or extend values in storage for current User+Chat."""
    async with dp.current_state().proxy() as udata:
        for key, value in new_data.items():

            # extend value with list
            if isinstance(value, list):
                udata.setdefault(key, [])
                udata[key].extend(value)

            # delete value if empty tuple passed
            elif isinstance(value, tuple) and not value:
                del udata[key]

            else:  # just set value
                udata[key] = value
