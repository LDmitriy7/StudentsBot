from aiogram import types


def get_file_obj(msg: types.Message):
    if msg.content_type == 'photo':
        file_id = msg.photo[-1].file_id
    elif msg.content_type == 'document':
        file_id = msg.document.file_id
    else:
        raise TypeError('Forbidden file type')

    return msg.content_type, file_id
