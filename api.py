import asyncio
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


@asyncio.coroutine
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

        individualInsert = insertingClass(itemArray, category, source)
        individualInsert.individualInsertObj()


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
        print(self.source)


# Individual insertion fucntion


def got_result(future):

    return future.result()


loop = asyncio.get_event_loop()

tasks = [
    Type1parser("http://feeds.reuters.com/reuters/INtopNews",
                "Reuters India", "General", "Top"),
    Type1parser("https://www.theguardian.com/world/rss",
                "The Guardian", "World", "Top")]

# name = future1.add_done_callback(got_result)
# age = future2.add_done_callback(got_result)

loop.run_until_complete(asyncio.wait(tasks))
loop.close()
