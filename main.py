#!/usr/bin/env python
import feedparser # pip install feedparser
from pymongo import MongoClient
import json
import re
import datetime

def Type1parser(url,source,category,tag):
    """

    This class handles all the feed parsing jobs initialted by the main function

    """


    feed = feedparser.parse(url)
    posts = []
    for item in feed['entries']:


        summarys=""
        if 'summary' in item:
            summarys=item.summary
        publishedTag=""
        if 'published' in item:
            publishedTag=item.published
        if 'media_content' in item:
             posts.append({
            'title': item.title,
            'summary': summarys,
            'link': item.link,
            'image':item.media_content[0]['url'],
            'published':publishedTag,
            'source':source,
            'category':category,
            'type':tag
        })

        print(item.title)
    # print(json.dumps(posts))







def main():
    """  Calling the main class parser for appropriate  rss feeds """


    Type1parser("http://rss.cnn.com/rss/edition.rss","CNN","General","Top")
    Type1parser("http://rss.cnn.com/rss/edition_world.rss","CNN","World","Top")
    Type1parser("http://rss.cnn.com/rss/edition_technology.rss","CNN","Technology","Top")
    Type1parser("http://rss.cnn.com/rss/edition_space.rss","CNN","Science","Top")
    Type1parser("http://rss.cnn.com/rss/edition_entertainment.rss","CNN","Entertainment","Top")
    Type1parser("http://rss.cnn.com/rss/cnn_latest.rss","CNN","General","Latest")
    print("\n")


    Type1parser("http://feeds.bbci.co.uk/news/rss.xml","BBC","General","Top")
    Type1parser("http://feeds.bbci.co.uk/news/world/rss.xml","BBC","World","Top")
    Type1parser("http://feeds.bbci.co.uk/news/politics/rss.xml","BBC","Politics","Top")
    Type1parser("http://feeds.bbci.co.uk/news/business/rss.xml","BBC","Business","Top")
    Type1parser("http://feeds.bbci.co.uk/news/health/rss.xml","BBC","Health","Top")
    Type1parser("http://feeds.bbci.co.uk/news/education/rss.xml","BBC","Education","Top")
    Type1parser("http://feeds.bbci.co.uk/news/science_and_environment/rss.xml","BBC","Science","Top")
    Type1parser("http://feeds.bbci.co.uk/news/technology/rss.xml","BBC","Technology","Top")
    Type1parser("http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml","BBC","Entertainment","Top")







if __name__  ==  '__main__':
    main()
