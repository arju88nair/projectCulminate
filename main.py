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
        type
        ):
        self.url = url
        self.source = source
        self.category = category
        self.type = type

    def call_url(self):
        urlSelf = str(self.url)
        r = requests.get(self.url).json()
        if 'articles' in r:
        	logger.info(self.url)

        	contents = r['articles']
        	array = []
	        for i in contents:
	            Rake = RAKE.Rake('stopwords_en.txt')  # takes stopwords as list of strings
	            words = Rake.run(i['title'])
	            tagWordArray = []
	            for word in words:
	                tagWordArray.append(word[0].title())
	            itemArray = dict()
	            itemArray['title'] = i['title']
	            itemArray['author'] = i['author']
	            itemArray['description'] = i['description']
	            itemArray['url'] = i['url']
	            itemArray['urlToImage'] = i['urlToImage']
	            itemArray['publishedAt'] = i['publishedAt']
	            itemArray['tags'] = tagWordArray
	            itemArray['created_at'] = str(datetime.now())
	            itemArray['source'] = self.source
	            itemArray['category'] = self.category          
	            itemArray['type'] = self.type          
	            itemArray['uTag'] = str(i['publishedAt']) + self.source.replace(" ", "")

	            array.append(itemArray)

	        insert = mongo.db.tempMain.insert_many(array).inserted_ids
	        if insert:
	            logger.info('Inserted for ' + self.source + ' of type ' + self.type 
	                        + str(datetime.now()))
	            return  "hi"

	        else:

	            logger.info('Error in insertion for '+ self.source + ' of type ' + self.type 
	                        + str(datetime.now()))
	            return "bye"



# URL classifying class

class primaryUrlClass:

    def __init__(self, url,name,category):
        self.url = url
        self.name = name
        self.category = category

    def callScrapping(self):
        url = self.url + 'top&apiKey=' + api_key
        ApiCallTop = scrapping(url, self.name, self.category,"top")
        ApiCallTopResponse = ApiCallTop.call_url()
        return ApiCallTopResponse
        url = self.url + 'latest&apiKey=' + api_key
        ApiCallLatest = scrapping(url, self.name, self.category,"latest")
        ApiCallLatestRes = ApiCallLatest.call_url
        return ApiCallLatestRes
        url = self.url + 'popular&apiKey=' + api_key
        ApiCallpopular = scrapping(url, self.name, self.category,"popular")
        ApiCallpopularResponse = ApiCallpopular.call_url
        return ApiCallpopularResponse



# Main route

@app.route('/', methods=['GET'])
def first_route():


    primeURLCallCNN = \
        primaryUrlClass('https://newsapi.org/v1/articles?source=cnn&sortBy=',"CNN","General"
                        )
    return(primeURLCallCNN.callScrapping())


    # primeURLCallNextWeb = \
    #     primaryUrlClass(' https://newsapi.org/v1/articles?source=the-next-web&sortBy=',"The Next Web","Technology"
    #                     )
    # return(primeURLCallNextWeb.callScrapping())





if __name__ == '__main__':
    app.run(debug=True)

