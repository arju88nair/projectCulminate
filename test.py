

import threading
import time
import feedparser  # pip install feedparser


start = time.time()
urls = [["http://feeds.reuters.com/reuters/INtopNews", "General"],
        ["http://feeds.reuters.com/reuters/INentertainmentNews", "Blah"]]


def fetch_url(url):
    feed = feedparser.parse(url[0])
    array = []
    for item in feed['entries']:
        print(item.title)


threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print ("Elapsed Time: %s" % (time.time() - start))
