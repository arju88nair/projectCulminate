#!/usr/bin/env python
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


logging.basicConfig(filename='logger.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


connection = MongoClient('mongodb://localhost:27017/Culminate')
db = connection.Culminate

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
                    logging.info('Inserted new for ' + tag + "   for  " + source
                                 )
                    logging.info('\n')
                else:
                    logging.info('Error in insertion for ' +
                                 tag + "   for  " + source)
                    logging.info('\n')

    print("Done for " + tag + " for " + source)
# Parsing function


def Type1parser(url, source, category, tag):
    """

    This class handles all the feed parsing jobs initialted by the main function

    """

    feed = feedparser.parse(url)
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


# main function

def main():
    start = time.time()

    """  Calling the main class parser for appropriate  rss feeds """


def main():
    """  Calling the main class parser for appropriate  rss feeds """

    # Type1parser("http://rss.cnn.com/rss/edition.rss", "CNN", "General", "Top")

    # Type1parser("http://rss.cnn.com/rss/edition_world.rss",
    #             "CNN", "World", "Top")
    # Type1parser("http://rss.cnn.com/rss/edition_technology.rss",
    #             "CNN", "Technology", "Top")
    # Type1parser("http://rss.cnn.com/rss/edition_space.rss",
    #             "CNN", "Science", "Top")
    # Type1parser("http://rss.cnn.com/rss/edition_entertainment.rss",
    #             "CNN", "Entertainment", "Top")
    # Type1parser("http://rss.cnn.com/rss/cnn_latest.rss",
    #             "CNN", "General", "Latest")

    # Type1parser("http://feeds.bbci.co.uk/news/rss.xml",
    #             "BBC", "General", "Top")
    # Type1parser("http://feeds.bbci.co.uk/news/world/rss.xml",
    #             "BBC", "World", "Top")
    # Type1parser("http://feeds.bbci.co.uk/news/politics/rss.xml",
    #             "BBC", "Politics", "Top")
    # Type1parser("http://feeds.bbci.co.uk/news/business/rss.xml",
    #             "BBC", "Business", "Top")
    # Type1parser("http://feeds.bbci.co.uk/news/health/rss.xml",
    #             "BBC", "Health", "Top")
    # Type1parser("http://feeds.bbci.co.uk/news/education/rss.xml",
    #             "BBC", "Education", "Top")
    # Type1parser("http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    #             "BBC", "Science", "Top")
    # Type1parser("http://feeds.bbci.co.uk/news/technology/rss.xml",
    #             "BBC", "Technology", "Top")
    # Type1parser("http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
    #             "BBC", "Entertainment", "Top")

# Times of India

    # Type1parser("http://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    #             "Times of India", "General", "Top")

# New York Times

    # Type1parser("http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    #             "New York Times", "General", "Top")

    # Type1parser("http://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    #             "New York Times", "World", "Top")

    # Type1parser("http://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    #             "New York Times", "Business", "Top")

    # Type1parser("http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    #             "New York Times", "Technology", "Top")

    # Type1parser("http://rss.nytimes.com/services/xml/rss/nyt/Sports.xml",
    #             "New York Times", "Sports", "Top")

    # Type1parser("http://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    #             "New York Times", "Science", "Top")

    # Type1parser("http://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
    #             "New York Times", "Health", "Top")


# Reuters

    Type1parser("http://feeds.reuters.com/reuters/INtopNews",
                "Reuters India", "General", "Top")
    Type1parser("http://feeds.reuters.com/reuters/INbusinessNews",
                "Reuters India", "Business", "Top")
    Type1parser("http://feeds.reuters.com/reuters/INsouthAsiaNews",
                "Reuters India", "World", "Top")
    Type1parser("http://feeds.reuters.com/reuters/INworldNews",
                "Reuters India", "World", "Top")
    Type1parser("http://feeds.reuters.com/reuters/INentertainmentNews",
                "Reuters India", "Entertainment", "Top")
    Type1parser("http://feeds.reuters.com/reuters/INsportsNews",
                "Reuters India", "Sports", "Top")
    Type1parser("http://feeds.reuters.com/reuters/INcricketNews",
                "Reuters India", "Sports", "Top")
    Type1parser("http://feeds.reuters.com/reuters/INtechnologyNews",
                "Reuters India", "Technology", "Top")
    Type1parser("http://feeds.reuters.com/reuters/INhealth",
                "Reuters India", "Health", "Top")


# The Guardian
    Type1parser("https://www.theguardian.com/world/rss",
                "The Guardian", "World", "Top")
    Type1parser("https://www.theguardian.com/international/rss",
                "The Guardian", "General", "Top")
    Type1parser("https://www.theguardian.com/uk/environment/rss",
                "The Guardian", "World", "Top")
    Type1parser("https://www.theguardian.com/uk/money/rss",
                "The Guardian", "Business", "Top")
    Type1parser("https://www.theguardian.com/uk/business/rss",
                "The Guardian", "Business", "Top")
    Type1parser("https://www.theguardian.com/uk/technology/rss",
                "The Guardian", "Technology", "Top")
    Type1parser("https://www.theguardian.com/uk/sport/rss",
                "The Guardian", "Sports", "Top")
    Type1parser("https://www.theguardian.com/world/rss",
                "The Guardian", "General", "Top")

    print ('It took', time.time() - start, 'seconds.')


if __name__ == '__main__':
    main()
