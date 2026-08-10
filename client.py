import aiohttp
import asyncio
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()
headers = {
    "User-Agent": ua.random,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}

async def send_data():
    semaphore = asyncio.Semaphore(2)
    async with aiohttp.ClientSession() as session:
        urls = [f"https://books.toscrape.com/catalogue/page-{page}.html" for page in range(1, 4)]
        tasks = [dev(url, session, semaphore) for url in urls]
        await asyncio.gather(*tasks)
async def dev(url, session, semaphore):
        try:
            async with semaphore:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        print(f'Подключение успешно! {response.status}')
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        html_data = soup.find_all('article', class_="product_pod")
                    for get_html_data in html_data:
                        product_id = get_html_data.find('h3').find('a')["title"]
                        price = get_html_data.find('p', class_='price_color').text
                        clean_price = float(price.replace('£', '').strip())
                        article = product_id[:10].strip().replace(" ", "_")
                        async with session.post("http://127.0.0.1:8000/api/v1/ingest", json={
                            "product_id": article,
                            "price": clean_price,
                            "category": "Books",
                            "discount": 0
                        }) as response:
                            print(f"Книга '{article}' отправлена. Статус: {response.status}")
                            print(f"Ответ от FastAPI: {await response.json()}")
                    else:
                        raise Exception(f'Сайт-донор вернул ошибку. Статус: {response.status}')
        except Exception as e:
            print(f'Критическая ошибка. {e}')
if __name__ == "__main__":
    asyncio.run(send_data())

#Step 2: python client.py