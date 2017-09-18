#!/usr/bin/env python
import feedparser # pip install feedparser
import asyncio


async def get(url):
    print("Start: %s" % url)
    response = await feedparser.parse(url)
    print("Finish: %s" % url)
    response.close()
    return 1


async def run_all(url1, url2):
    r1 = get(url1)
    r2 = get(url2)
    results = await asyncio.gather(r1, r2)

    for res in results:
        print(res)


loop = asyncio.get_event_loop()
loop.run_until_complete(run_all("http://rss.cnn.com/rss/edition.rss", "http://rss.cnn.com/rss/edition_world.rss"))
loop.close()

# from pymongo import MongoClient

# def Type1parser(url,source,category,type):
#     d = feedparser.parse(url)

#     for item in d['items']:
#         if  'description' in item:
#             print(item['description'])


#         print("\n")




# def main():
#     Type1parser("http://rss.cnn.com/rss/edition.rss","CNN","General","Latest")






# if __name__  ==  '__main__':
#     main()
