from aiogram.utils.helper import Constants


class ProjectStatuses(Constants):
    ACTIVE = 'Активен'
    IN_PROGRESS = 'Выполняется'
    COMPLETED = 'Выполнен'
    # REVIEWED = 'Оставлен отзыв'


class UserRoles(Constants):
    client = ...
    worker = ...


class SendTo(Constants):
    CHANNEL = ...
    WORKER = ...


if __name__ == '__main__':
    print(ProjectStatuses.all)
    print(UserRoles.all)
    print(SendTo.all)
