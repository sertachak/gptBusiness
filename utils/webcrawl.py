import asyncio
import os.path
from urllib.parse import urlparse
from dotenv import load_dotenv
import aiohttp
from bs4 import BeautifulSoup


load_dotenv()
proxyUrl = "https://api.proxyscrape.com/v2/account/datacenter_shared/proxy-list?auth={}&type=getproxies&country[]=all&protocol=http&format=normal&status=all".format(os.environ.get("PROXY_AUTH_KEY"))


async def fetch_all(session, urls, proxyList):
    tasks = []
    for proxy in proxyList:
        for url in urls:
            task = await session.get(url, proxy=proxy)
            if task.status != 200:
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
    proxyList = []

    async with aiohttp.ClientSession as session:
        proxyList = await session.get(proxyUrl)



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
        htmls = await fetch_all(session, links, proxyList)

    for html in htmls:
        # Get the next URL from the queue
        # print(html)  # for debugging and to see the progress

        # Save text from the url to a <url>.txt file
        with open(
                "text/" + local_domain + "/" + html["url"][8:].replace("/", "_") + ".txt",
                "w",
        ) as f:
            # Get the text from the URL using BeautifulSoup
            soup = BeautifulSoup(html["text"], "html.parser")

            # Get the text but remove the tags
            text = soup.get_text()

            # If the crawler gets to a page that requires JavaScript, it will stop the crawl
            if "You need to enable JavaScript to run this app." in text:
                print(
                    "Unable to parse page " + url + " due to JavaScript being required"
                )

            # Otherwise, write the text to the file in the text directory
            f.write(text)