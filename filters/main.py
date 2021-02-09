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

    def __init__(self, qprefix: str):
        self.qprefix = qprefix

    def __call__(self, query: types.CallbackQuery):
        if query.data.startswith(self.qprefix):
            payload = query.data.replace(self.qprefix, '')
            return {'payload': payload}
        else:
            return False


class InlinePrefix:
    """Check query.query for prefix, return payload without prefix."""

    def __init__(self, iprefix: str):
        self.iprefix = iprefix

    def __call__(self, query: types.InlineQuery):
        if query.query.startswith(self.iprefix):
            payload = query.query.replace(self.iprefix, '')
            return {'payload': payload}
        else:
            return False
