# import asyncio
# import feedparser  # pip install feedparser
# import time
# start = time.time()


# async def compute(url):
#     feed = feedparser.parse(url)
#     array = []
#     for item in feed['entries']:
#         return item.title


# async def print_sum(url):
#     result = await compute(url)
#     print(result)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.gather(print_sum("http://feeds.reuters.com/reuters/INtopNews"), print_sum("http://feeds.reuters.com/reuters/INentertainmentNews"))
#                         )
# loop.close()
# print ('It took', time.time() - start, 'seconds.')
import asyncio


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print("Task %s: Compute factorial(%s)..." % (name, i))
        await asyncio.sleep(1)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    factorial("A", 2),
    factorial("B", 3),
    factorial("C", 4),
))
loop.close()
