from keyboards.inline_plain import find_subject, work_types, balance, subjects, change_profile

keyboards = [find_subject, work_types, balance, subjects, change_profile]

for kb in keyboards:
    for row in kb.inline_keyboard:
        a = [f'{i.text} ({i.callback_data})' for i in row]
        print(a)
    print()
