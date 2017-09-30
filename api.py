import feedparser  # pip install feedparser
import time
start = time.time()


def compute(url):
    feed = feedparser.parse(url)
    array = []
    for item in feed['entries']:
        return item.title


def print_sum():
    urls = ["http://feeds.reuters.com/reuters/INtopNews",
            "http://feeds.reuters.com/reuters/INentertainmentNews"]
    for url in urls:
        print(compute(url))


if __name__ == '__main__':
    print_sum()

print ('It took', time.time() - start, 'seconds.')
