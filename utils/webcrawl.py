import asyncio
import os.path
from urllib.parse import urlparse
from dotenv import load_dotenv
import aiohttp
from bs4 import BeautifulSoup


load_dotenv()


async def fetch_all(session, urls):
    tasks = []
    for url in urls:
        task = await session.get(url, proxy=os.getenv("LUMINATI_PROXY"))
        if task.status is not 200:
            continue
        response_text = await task.text()
        task_response = {
            "url": url,
            "text": response_text
        }
        tasks.append(task_response)

    results = asyncio.gather(*tasks)
    return results


async def crawl(url):
    local_domain = urlparse(url).netloc

    if not os.path.exists("/text"):
        os.mkdir("/text")

    if not os.path.exists("/text" + local_domain + "/"):
        os.mkdir("/text" + local_domain + "/")

    if not os.path.exists("processed"):
        os.mkdir("processed")

    links = []
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url + "/sitemap.xml", proxy=os.getenv("LUMINATI_PROXY")
        ) as response:
            # Parse the XML
            soup = BeautifulSoup(await response.text(), "html.parser")
            for link in soup.find_all("loc"):
                link = link.text
                links.append(link)

    async with aiohttp.ClientSession as session:
        response = await fetch_all(session, links)
