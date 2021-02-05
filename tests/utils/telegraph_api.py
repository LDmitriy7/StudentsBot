from utils.telegraph_api import make_html_content, create_page
import asyncio

invite_project_url = 'https://t.me/test2_test_bot?start=offer_project_724477101'
works = ['https://docs.aiohttp.org/en/stable/_static/aiohttp-icon-128x128.png']
html_content = make_html_content(0, 'Я python-программист', [], invite_project_url, works, [])


async def main():
    resp = await create_page('Test3', html_content)
    print(resp)


asyncio.get_event_loop().run_until_complete(main())
