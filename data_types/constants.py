from aiogram.utils.helper import Constants


class TextQueries(Constants):
    INVITE_PROJECT = ...  # для инлайн-запроса на приглашение в проект
    DEL_MESSAGE = ...  # для удаления связанного сообщения
    REFUSE_WORK_PRICE = ...  # для отказа от предложенной цены


class Prefixes(Constants):
    """Command-prefixes for deep-links and query.data"""
    GET_PROJECT_ = ...  # для получения проекта
    DEL_PROJECT_ = ...  # для запроса удаления проекта
    TOTAL_DEL_PROJECT_ = ...  # для удаления проекта
    PAY_FOR_PROJECT_ = ...  # для оплаты проекта
    INVITE_PROJECT_ = ...  # для предложения проекта автором
    OFFER_PROJECT_ = ...  # для предложения проекта заказчиком
    PICK_PROJECT_ = ...  # для принятия персонального проекта автором
    CONFIRM_PROJECT_ = ...  # для подтверждения выполнения проекта

    GET_FILES_ = ...  # для получения файлов к проекту

    SEND_BID_ = ...  # для заявки на проект
    PICK_BID_ = ...  # для принятия заявки


class ProjectStatuses(Constants):
    ACTIVE = 'Активен'
    IN_PROGRESS = 'Выполняется'
    COMPLETED = 'Выполнен'
    REVIEWED = 'Оставлен отзыв'


class UserRoles(Constants):
    client = ...
    worker = ...


class SendTo(Constants):
    CHANNEL = ...
    WORKER = ...
