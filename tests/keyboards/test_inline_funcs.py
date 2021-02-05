from keyboards.inline_funcs import link_button, for_project, del_project, for_bid

project_id = 'test123'

print(link_button('Ссылка', 'https://test.com'))
print(for_project(project_id, True, False, True, 'https://chat_link.com'))
print(del_project(project_id))
print(for_bid(project_id, True, True))
