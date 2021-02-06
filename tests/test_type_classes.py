from type_classes import Profile, Project, ProjectData, Account, Bid, Rating, Review, Chat
from pprint import pp

profile = Profile(**{
    "phone_number": None, "email": None, "biography": "Я пишу ботов на python 3 года", "works": [
        "AgACAgIAAxkBAAJGAAFgHIfs5JW3fuagseM8wysRP14TsAACI7MxG7Sa4UizlN7IoP8H2JLpMpsuAAMBAAMCAAN5AAOoQQIAAR4E"],
    "nickname": "LDmitriy7", "deals_amount": 0
})

account = Account(**{
    "_id": 724477101, "balance": 4800,
    "subjects": ["Земельное право", "Электротехника", "Ноксология", "Международное право",
                 "Ядерная медицина"],
    "page_url": "https://telegra.ph/Stranica-avtora-T7-02-03",
    'profile': profile
})

bid = Bid(**{
    "_id": {"$oid": "6016f6a74ca817b3e3f8fa7a"}, "client_id": 1478623483, "worker_id": 724477101,
    "project_id": "6016f6084ca817b3e3f8fa79", "text": "Здравствуйте, помогу прям сейчас"
})

chat = Chat(**{
    "_id": -541355717, "project_id": "6016f6084ca817b3e3f8fa79", "chat_type": "client", "user_id": 1478623483,
    "link": "https://t.me/joinchat/IERuxYC7bh_h4wTL", "pair_id": -545651958
})

project_data = ProjectData(**{
    "work_type": "Практика", "subject": "Python", "date": "2021-02-18",
    "description": "Написать перцептрон на python", "price": 500,
    "note": "Не нужна", "files": [
        ["photo", "AgACAgIAAxkBAAI_jWAZdfa6_SNMPl4-rMEtmtBO6urBAAIRsjEbWpvQSBYwGt4F4Rsm7MBImC4AAwEAAwIAA3kAA9p_BgABHgQ"]
    ]
})

project = Project(**{
    "_id": {"$oid": "601975fd7a44a2358740a40e"}, "client_id": 1478623483, "worker_id": 724477101,
    "status": "Активен", "post_url": "t.me/help_students7/78", 'data': project_data,
    'client_chat_id': -541355717, 'worker_chat_id': -545651958
})

rating = Rating(**{
    "quality": 4, "contact": 5, "terms": 4
})

review = Review(**{
    "_id": {"$oid": "601bea5e20622f6689301c84"}, "client_id": 1478623483, "worker_id": 724477101,
    "project_id": "601975fd7a44a2358740a40e", "rating": rating, "text": "Спасибо!", "client_name": "Максим Некрасов"
})

pp(profile)
pp(account)
pp(bid)
pp(chat)
pp(project_data)
pp(project)
pp(rating)
pp(review)
