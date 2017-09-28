import asyncio
import requests


async def main():
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(
        None, requests.get, 'http://feeds.reuters.com/reuters/INtopNews')
    future2 = loop.run_in_executor(
        None, requests.get, 'https://www.theguardian.com/world/rss')
    response1 = await future1
    response2 = await future2
    print(response1.text)
    print(response2.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
