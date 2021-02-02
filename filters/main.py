from aiogram import types


class DeepLinkPrefix:
    """Check deep-link for prefix, return payload without prefix."""

    def __init__(self, dprefix: str):
        self.dprefix = dprefix

    def __call__(self, msg: types.Message):
        deeplink = msg.text.split()
        if deeplink[0] == '/start' and deeplink[-1].startswith(self.dprefix):
            payload = deeplink[-1].replace(self.dprefix, '')
            return {'payload': payload}
        else:
            return False


class QueryPrefix:
    """Check query.data for prefix, return payload without prefix."""

    def __init__(self, iprefix: str):
        self.iprefix = iprefix

    def __call__(self, query: types.CallbackQuery):
        if query.data.startswith(self.iprefix):
            payload = query.data.replace(self.iprefix, '')
            return {'payload': payload}
        else:
            return False


if __name__ == '__main__':
    GET_FILES_PREFIX = 'GET_FILES_'

    msg = types.Message()
    msg.text = '/start ' + GET_FILES_PREFIX + '2312312f'
    print(msg.text)
    _filter = DeepLinkPrefix(GET_FILES_PREFIX)
    result = _filter(msg)
    print(result)

    query = types.CallbackQuery()
    query.data = GET_FILES_PREFIX + '3287ssd3'
    print(query.data)
    _filter = QueryPrefix(GET_FILES_PREFIX)
    result = _filter(query)
    print(result)
