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


logging.basicConfig(filename='logger.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


connection = MongoClient('mongodb://localhost:27017/Culminate')
db = connection.Culminate


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
        if self.data['category'] == "General":
            print(self.data['title'])
            if not db.generalMain.find({"uTag": str(self.data['uTag'])}).count() > 0:
                # if db.generalMain.count() == 0:
                #     insertDoc = db.generalMain.insert_one(self.data)
                for document in db.generalMain.find():
                    print(self.data['title'])
                    print("\n")
                    collision = fuzz.token_sort_ratio(
                        str(self.data['title']), document['title'])
                    print(collision)
                    if int(collision) < 50:
                        print("d")
                        insertDoc = db.generalMain.insert_one(self.data)
                        if insertDoc:
                            logging.info('Insert new for general')
                            logging.info('\n')
                        else:
                            logging.info('Error in insertion for general')
                            logging.info('\n')

    def tempTablePush(self):
        """
        Here it is inserted  in the temptable for future classification and insertion

        """
        insert = db.tempMain.insert_many(self.data).inserted_ids
        if insert:
            logger.info('Inserted for ' + self.source + ' of type '
                        + str(self.category) + '' + str(datetime.now()) + ' in tempMain ')
            logging.info('\n')
        else:

            logger.warning('Error in insertion for ' + self.source
                           + ' of type ' + self.category + ' in tempMain '
                           + str(datetime.now()))
            logging.warning('\n')


def Type1parser(url, source, category, tag):
    """

    This class handles all the feed parsing jobs initialted by the main function

    """

    feed = feedparser.parse(url)
    array = []
    for item in feed['entries']:

        summarys = ""
        if 'summary' in item:
            summarys = item.summary
        publishedTag = ""
        if 'published' in item:
            publishedTag = item.published
        if 'media_content' in item:
            # takes stopwords as list of strings
            Rake = RAKE.Rake('stopwords_en.txt')
            words = Rake.run(item.title)
            tagWordArray = []
            for word in words:
                tagWordArray.append(word[0].title())
            itemArray = dict()
            itemArray['title'] = item.title
            itemArray['summary'] = summarys
            itemArray['link'] = item.link
            itemArray['image'] = item.media_content[0]['url']
            itemArray['published'] = publishedTag
            itemArray['source'] = source
            itemArray['type'] = tag
            itemArray['category'] = category
            itemArray['tags'] = tagWordArray
            itemArray['created_at'] = str(datetime.now())
            itemArray['uTag'] = hashlib.sha256(
                str(item.title).encode('utf-8')).hexdigest()[:16]
            individualInsert = insertingClass(itemArray, category, source)
            individualInsert.individualInsertObj()

        # insertingClassObject=insertingClass(itemArray,category)
        # insertingClassObject.mainClassObj()
        # return "hi";

    # print(json.dumps(posts))


# main function

def main():
    """  Calling the main class parser for appropriate  rss feeds """

    Type1parser("http://rss.cnn.com/rss/edition.rss", "CNN", "General", "Top")
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

    # print("\n")

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


if __name__ == '__main__':
    main()
