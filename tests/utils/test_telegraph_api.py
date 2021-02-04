from utils.telegraph_api import make_html_content, create_page

invite_project_url = 'https://t.me/test2_test_bot?start=offer_project_724477101'
html_content = make_html_content(0, 'Я python-программист', [], invite_project_url, [], [])
print(create_page('Test3', html_content))
