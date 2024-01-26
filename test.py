import asyncio
from pyppeteer import launch

async def scrape_website(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'domcontentloaded'})
    await page.content()
    title = await page.evaluate('document.title')
    print(f'Title: {title}')

    all_links = await page.querySelectorAll('a')
    print(f'Found {len(all_links)} links')

    for link in all_links:
        href = await (await link.getProperty('href')).jsonValue()
        if "?v=" in href:
            print(href)
            break

    await browser.close()

if __name__ == '__main__':
    url = 'https://www.youtube.com/results?search_query=hello'
    asyncio.get_event_loop().run_until_complete(scrape_website(url))
