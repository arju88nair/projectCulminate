#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import requests
import json
from datetime import datetime
import RAKE





app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'Culminate'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Culminate'

mongo = PyMongo(app)

class scrapping:

    def __init__(self, url, source,category):
        self.url = url
        self.source = source
        self.category = category

    def call_url(self):
        headers = {'Accept': 'application/json'}
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
            itemArray['created_at']=str(datetime.now())
            itemArray['source']=self.source
            itemArray['category']=self.category
            array.append(itemArray)

        
          
        insert=mongo.db.tempMain.insert_many(array).inserted_ids
        if insert:
        	return "Successfully inserted"
        else:
            return "Something went wrong"	




@app.route('/', methods=['GET'])
def first_route():
    prime_call = \
        scrapping('https://newsapi.org/v1/articles?source=cnn&sortBy=top&apiKey=e428fe12b6ea434ca78b3c3d3e705c15'
                  , 'CNN News','General')
    prime_call_response = prime_call.call_url()
    return jsonify(prime_call_response)

if __name__ == '__main__':
    app.run(debug=True)

