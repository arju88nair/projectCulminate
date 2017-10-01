from multiprocessing import Pool
import time
import feedparser  # pip install feedparser


start = time.time()


def compute(url):
    feed = feedparser.parse(url)
    array = []
    for item in feed['entries']:
        return item.title


if __name__ == '__main__':
    p = Pool(500)
    print(p.map(compute, ["http://feeds.reuters.com/reuters/INtopNews",
                          "http://feeds.reuters.com/reuters/INentertainmentNews"]))
    print ("Elapsed Time: %s" % (time.time() - start))
