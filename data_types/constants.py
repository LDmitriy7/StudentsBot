from aiogram.utils.helper import Helper, Item, HelperMode


class Prefixes(Helper):
    """Command-prefixes for deep-links and query.data"""
    GET_PROJECT_ = Item()  # для получения проекта
    DEL_PROJECT_ = Item()  # для запроса удаления проекта
    TOTAL_DEL_PROJECT_ = Item()  # для удаления проекта
    PAY_FOR_PROJECT_ = Item()  # для оплаты проекта
    INVITE_PROJECT_ = Item()  # для предложения проекта автором
    OFFER_PROJECT_ = Item()  # для предложения проекта заказчиком
    PICK_PROJECT_ = Item()  # для принятия персонального проекта автором
    CONFIRM_PROJECT_ = Item()  # для подтверждения выполнения проекта

    GET_FILES_ = Item()  # для получения файлов к проекту

    SEND_BID_ = Item()  # для заявки на проект
    PICK_BID_ = Item()  # для принятия заявки


class ProjectStatuses(Helper):
    ACTIVE = 'Активен'
    IN_PROGRESS = 'Выполняется'
    COMPLETED = 'Выполнен'
    REVIEWED = 'Оставлен отзыв'


class UserRoles(Helper):
    mode = HelperMode.lowercase
    CLIENT = Item()
    WORKER = Item()


class SendTo(Helper):
    CHANNEL = Item()
    WORKER = Item()
