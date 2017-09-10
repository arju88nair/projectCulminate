#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import requests
import json
import time
from calendar import timegm
from datetime import datetime
import RAKE
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'Culminate'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Culminate'

mongo = PyMongo(app)
api_key = str('e428fe12b6ea434ca78b3c3d3e705c15')


# Scrapping Class

class scrapping:

    def __init__(
        self,
        url,
        source,
        category,
        ):
        self.url = url
        self.source = source
        self.category = category

    def call_url(self):
        urlSelf = str(self.url)
        r = requests.get(self.url).json()
        contents = r['articles']
        array = []
        for i in contents:
            Rake = RAKE.Rake('stopwords_en.txt')  # takes stopwords as list of strings
            words = Rake.run(i['title'])
            tagWordArray = []
            for word in words:
                tagWordArray.append(word[0].title())
            itemArray = dict()
            itemArray['title'] = i['author']
            itemArray['author'] = i['title']
            itemArray['description'] = i['description']
            itemArray['url'] = i['url']
            itemArray['urlToImage'] = i['urlToImage']
            itemArray['publishedAt'] = i['publishedAt']
            itemArray['tags'] = tagWordArray
            itemArray['created_at'] = str(datetime.now())
            itemArray['source'] = self.source
            itemArray['category'] = self.category
            utc_time = time.strptime(i['publishedAt'],
                    '%Y-%m-%dT%H:%M:%SZ')
            epoch_time = timegm(utc_time)
            itemArray['uTag'] = str(epoch_time) + self.source.replace(" ", "")

            array.append(itemArray)

        insert = mongo.db.tempMain.insert_many(array).inserted_ids
        if insert:
            logger.info('Inserted for ' + self.source + ' '
                        + str(datetime.now()))
        else:

            logger.info('Error in insertion for ' + self.source + ' '
                        + str(datetime.now()))


# URL classifying class

class primaryUrlClass:

    def __init__(self, url):
        self.type = type
        self.url = url

    def callScrapping(self):
        url = self.url + 'top&apiKey=' + api_key
        ApiCallTop = scrapping(url, 'CNN News', 'General')
        ApiCallTopResponse = ApiCallTop.call_url()
        url = self.url + 'latest&apiKey=' + api_key
        ApiCallLatest = scrapping(url, 'CNN News', 'General')
        ApiCallLatestRes = ApiCallLatest.call_url
        url = self.url + 'popular&apiKey=' + api_key
        ApiCallpopular = scrapping(url, 'CNN News', 'General')
        ApiCallpopularResponse = ApiCallpopular.call_url



# Main route

@app.route('/', methods=['GET'])
def first_route():

    # prime_call = \
    #     scrapping('https://newsapi.org/v1/articles?source=cnn&sortBy=top&apiKey='+ api_key
    #               , 'CNN News','General')
    # prime_call_response = prime_call.call_url()

    primeURLCall = \
        primaryUrlClass('https://newsapi.org/v1/articles?source=cnn&sortBy='
                        )
    return jsonify(primeURLCall.callScrapping())

if __name__ == '__main__':
    app.run(debug=True)

