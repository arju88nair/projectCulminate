

import threading
import feedparser  # pip install feedparser
from pymongo import MongoClient
import json
import re
import datetime
import logging
import RAKE
from calendar import timegm
from datetime import datetime
import hashlib
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup
import time


start = time.time()


logging.basicConfig(filename='logger.log', level=logging.INFO)
logger = logging.getLogger(__name__)


connection = MongoClient('mongodb://localhost:27017/Culminate')
db = connection.Culminate

logging.info('Started ' + str(datetime.now()))
# Main class


class insertingClass:
    """
    insertingClass does various sorting and inserting data to appropriate collections
    @params data : contains the data
    @params category : the category of the data
    @params source :the source of the data

     """

    def __init__(self, data, category, source):
        self.data = data
        self.category = category
        self.source = source

    def individualInsertObj(self):
        """

        Classifying according to the category

        """

        if self.data['category'] == "General":
            collectionInsert(db.General, "General", self.data, self.source)
        if self.data['category'] == "Technology":
            collectionInsert(db.Technology, "Technology",
                             self.data, self.source)
        if self.data['category'] == "Science":
            collectionInsert(db.Science, "Science", self.data, self.source)
        if self.data['category'] == "Entertainment":
            collectionInsert(db.Entertainment, "Entertainment",
                             self.data, self.source)
        if self.data['category'] == "World":
            collectionInsert(db.World, "World", self.data, self.source)
        if self.data['category'] == "Politics":
            collectionInsert(db.Politics, "Politics", self.data, self.source)
        if self.data['category'] == "Business":
            collectionInsert(db.Business, "Business", self.data, self.source)
        if self.data['category'] == "Health":
            collectionInsert(db.Health, "Health", self.data, self.source)
        if self.data['category'] == "Education":
            collectionInsert(db.Education, "Education", self.data, self.source)
        if self.data['category'] == "Sports":
            collectionInsert(db.Sports, "Sports", self.data, self.source)

# Individual insertion fucntion


def collectionInsert(collectionName, tag, data, source):
    """

    Inserting  function with respect to the collection name parsed

    """

    if collectionName.count() == 0:
        collectionName.insert_one(data)
    else:
        for document in collectionName.find():
            collision = fuzz.token_sort_ratio(
                str(data['title']), document['title'])
            tags = str(data['uTag'])
            if collectionName.find_one(
                    {'uTag': tags}, {'_id': 1}):
                pass
            else:
                insertDoc = collectionName.insert_one(data)
            if db.Main.find_one(
                    {'uTag': tags}, {'_id': 1}):
                pass
            else:
                insertDoc = db.Main.insert_one(data)
                if insertDoc:
                    logging.debug('Inserted new for ' + tag + "   for  " + source
                                 )
                    logging.debug('\n')
                else:
                    logging.debug('Error in insertion for ' +
                                 tag + "   for  " + source)
                    logging.debug('\n')

    print("Done for " + tag + " for " + source)
# Parsing function


def Type1parser(url, source, category, tag):
    """

    This class handles all the feed parsing jobs initialted by the main function

    """
    feed = eTagCheck(url, source)

    if feed != 304:
        array = []
        for item in feed['entries']:

            summarys = ""
            if 'summary' in item:
                cleantext = BeautifulSoup(item.summary).text

                summarys = cleantext
            publishedTag = ""
            if 'published' in item:
                publishedTag = item.published
                # if 'media_content' in item:
                # takes stopwords as list of strings
            Rake = RAKE.Rake('stopwords_en.txt')
            words = Rake.run(item.title)
            tagWordArray = []
            for word in words:
                tagWordArray.append(word[0].title())
            itemArray = dict()
            itemArray['title'] = item.title
            itemArray['link'] = item.link
            if 'media_content' in item:
                itemArray['image'] = item.media_content[0]['url']
            if 'media_thumbnail' in item:
                itemArray['image'] = item.media_thumbnail[0]['url']
            if source == "The Guardian":
                if 'media_content' in item:
                    if len(item.media_content) > 1:
                        itemArray['image'] = item.media_content[1]['url']
                    else:
                        itemArray['image'] = item.media_content[0]['url']

            itemArray['published'] = publishedTag
            itemArray['source'] = source
            itemArray['type'] = tag
            itemArray['category'] = category
            itemArray['summary'] = summarys
            itemArray['tags'] = tagWordArray
            itemArray['created_at'] = str(datetime.now())
            itemArray['uTag'] = hashlib.sha256(
                str(item.title).encode('utf-8')).hexdigest()[:16]

            print("Inside iterating loop")
            individualInsert = insertingClass(itemArray, category, source)
            individualInsert.individualInsertObj()
    else:
        print("304")
        logging.debug("304 for  " + url[0])


def eTagCheck(url, source):
    """
        eTagCheck determines if the feed is new or already processed
        @params url : contains the url
     """
    d = feedparser.parse(url)
    if hasattr(d, 'etag'):
        entry = db.feeds.find_one({"feed": url})
        if entry:
            logging.debug("Entry for  " + url)
            eTag = entry['eTag']
            db.feeds.update_one(
                {"feed": url},
                {
                    "$set": {"eTag": d.etag},
                },
                upsert=True,
            )
            feeds = feedparser.parse(url, etag=eTag)
            if hasattr(feeds,'status'):
                if feeds.status == 304:
                    logging.debug("304 in eTagcheck for  " + url)
                    return 304
                else:
                    logging.debug("200 for  " + url)
                    return feeds
            else:
                return feeds


        else:
            logging.debug("New for  " + url[0])
            db.feeds.update_one(
                {"feed": url},
                {
                    "$set": {"eTag": d.etag},
                },
                upsert=True,
            )
            return feedparser.parse(url)
    else:
        return feedparser.parse(url)





urls = [
        ["https://www.theguardian.com/world/rss",
         "The Guardian", "World", "Top"],
        ["https://www.theguardian.com/international/rss",
         "The Guardian", "General", "Top"],
        ["https://www.theguardian.com / uk / environment / rss",
         "The Guardian", "World", "Top"],
        ["https://www.theguardian.com/uk/money/rss",
         "The Guardian", "Business", "Top"],
        ["https://www.theguardian.com/uk/business/rss",
         "The Guardian", "Business", "Top"],
        ["https://www.theguardian.com/uk/technology/rss",
         "The Guardian", "Technology", "Top"],
        ["https://www.theguardian.com/uk/sport/rss",
         "The Guardian", "Sports", "Top"],
        ["http://feeds.reuters.com/reuters/INtopNews",
         "Reuters India", "General", "Top"],
        ["http://feeds.reuters.com/reuters/INbusinessNews",
         "Reuters India", "Business", "Top"],
        ["http://feeds.reuters.com/reuters/INbusinessNews",
         "Reuters India", "Business", "Top"],
        ["http://feeds.reuters.com/reuters/INsouthAsiaNews",
         "Reuters India", "World", "Top"],
        ["http://feeds.reuters.com/reuters/INworldNews",
         "Reuters India", "World", "Top"],
        ["http://feeds.reuters.com/reuters/INentertainmentNews",
         "Reuters India", "Entertainment", "Top"],
        ["http://feeds.reuters.com/reuters/INsportsNews",
         "Reuters India", "Sports", "Top"],
        ["http://feeds.reuters.com/reuters/INcricketNews",
         "Reuters India", "Sports", "Top"],
        ["http://feeds.reuters.com/reuters/INtechnologyNews",
         "Reuters India", "Technology", "Top"],
        ["http://feeds.reuters.com/reuters/INhealth",
         "Reuters India", "Health", "Top"],
        ["http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
         "New York Times", "General", "Top"],
        ["http://rss.nytimes.com/services/xml/rss/nyt/World.xml",
         "New York Times", "World", "Top"],
        ["http://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
         "New York Times", "Business", "Top"],
        ["http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
         "New York Times", "Technology", "Top"],
        ["http://rss.nytimes.com/services/xml/rss/nyt/Sports.xml",
         "New York Times", "Sports", "Top"],
        ["http://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
         "New York Times", "Science", "Top"],
        ["http://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
         "New York Times", "Health", "Top"],
        ["http://timesofindia.indiatimes.com/rssfeedstopstories.cms",
         "Times of India", "General", "Top"],
        ["http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
         "BBC", "Entertainment", "Top"],
        ["http://feeds.bbci.co.uk/news/technology/rss.xml",
         "BBC", "Technology", "Top"],
        ["http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
         "BBC", "Science", "Top"],
        ["http://feeds.bbci.co.uk/news/education/rss.xml",
         "BBC", "Education", "Top"],
        ["http://feeds.bbci.co.uk/news/health/rss.xml",
         "BBC", "Health", "Top"],
        ["http://feeds.bbci.co.uk/news/business/rss.xml",
         "BBC", "Business", "Top"],
        ["http://feeds.bbci.co.uk/news/politics/rss.xml",
         "BBC", "Politics", "Top"],
        ["http://feeds.bbci.co.uk/news/world/rss.xml",
         "BBC", "World", "Top"],
        ["http://feeds.bbci.co.uk/news/rss.xml",
         "BBC", "General", "Top"],
        ["http://rss.cnn.com/rss/cnn_latest.rss",
         "CNN", "General", "Latest"],
        ["http://rss.cnn.com/rss/edition_entertainment.rss",
         "CNN", "Entertainment", "Top"],
        ["http://rss.cnn.com/rss/edition_space.rss",
         "CNN", "Science", "Top"],
        ["http://rss.cnn.com/rss/edition_technology.rss",
         "CNN", "Technology", "Top"],
        ["http://rss.cnn.com/rss/edition_world.rss",
         "CNN", "World", "Top"],
        ["http://rss.cnn.com/rss/edition.rss",
         "CNN", "General", "Top"],
        ["http://feeds.mashable.com/Mashable",
         "Mashable", "Technology", "Top"],
        ["https://feeds.feedburner.com/ndtvnews-top-stories",
         "NDTV", "General", "Top"],
        ["https://feeds.feedburner.com/ndtvnews-world-news",
         "NDTV", "World", "Top"],
        ["https://feeds.feedburner.com/ndtvsports-cricket",
         "NDTV", "Sports", "Top"],
        ["https://feeds.feedburner.com/ndtvnews-people",
         "NDTV", "General", "Top"],
        ["https://feeds.feedburner.com/ndtvnews-latest",
         "NDTV", "General", "Top"],
        ["https://feeds.feedburner.com/ndtvprofit-latest",
         "NDTV", "Business", "Top"],
        ["https://feeds.feedburner.com/gadgets360-latest",
         "NDTV", "Technology", "Top"],
        ["https://feeds.feedburner.com/ndtvnews-trending-news",
         "NDTV", "General", "Top"],
        ["https://feeds.feedburner.com/ndtvcooks-latest",
         "NDTV", "Health", "Top"],
        ["https://feeds.feedburner.com/ndtvnews-india-news",
         "NDTV", "General", "Top"],
        ["https://feeds.feedburner.com/ndtvsports-latest",
         "NDTV", "Sports", "Top"],
        ["http://www.thehindu.com/business/?service=rss",
         "The Hindu", "Business", "Top"],
        ["http://www.thehindu.com/?service=rss",
         "The Hindu", "General", "Top"],
        ["http://www.thehindu.com/news/international/?service=rss",
         "The Hindu", "World", "Top"],
        ["http://www.thehindu.com/news/?service=rss",
         "The Hindu", "General", "Top"],
        ["http://www.thehindu.com/news/national/?service=rss",
         "The Hindu", "World", "Top"],
        ["http://www.thehindu.com/sport/?service=rss",
         "The Hindu", "Sports", "Top"],
        ["http://www.thehindu.com/sci-tech/technology/?service=rss",
         "The Hindu", "Technology", "Top"],
        ["http://www.thehindu.com/business/?service=rss",
         "The Hindu", "Business", "Top"],
        ["http://www.thehindu.com/business/?service=rss",
         "The Hindu", "Business", "Top"],
        ["http://www.thehindu.com/business/?service=rss",
         "The Hindu", "Business", "Top"],
        ["http://www.thehindu.com/business/?service=rss",
         "The Hindu", "Business", "Top"],
        ["http://www.thehindu.com/business/?service=rss",
         "The Hindu", "Business", "Top"],
        ["http://www.thehindu.com/business/?service=rss",
         "The Hindu", "Business", "Top"],
        ["http://www.thehindu.com/business/?service=rss",
         "The Hindu", "Business", "Top"],
        ["http://rssfeeds.usatoday.com/usatoday-NewsTopStories",
         "USA Today", "World", "Top"],

        ]


threads = [threading.Thread(target=Type1parser, args=(
    url)) for url in urls]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()




print ("Elapsed Time: %s" % (time.time() - start))
