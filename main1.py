#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import time
from calendar import timegm
from datetime import datetime
import RAKE
import logging
import hashlib
from pymongo import MongoClient
from fuzzywuzzy import fuzz

logging.basicConfig(filename = 'logger.log',level = logging.DEBUG)
logger  =  logging.getLogger(__name__)


connection  =  MongoClient('mongodb://localhost:27017/Culminate')
db  =  connection.Culminate
api_key  =  str('e428fe12b6ea434ca78b3c3d3e705c15')


class scrapping:

    def __init__(
        self,
        url,
        source,
        category,
        type,
        ):

        self.url  =  url
        self.source  =  source
        self.category  =  category
        self.type  =  type

    def call_url(self):
        logger.debug(self.url)
        logging.info('\n')

        r  =  requests.get(self.url).json()
        if 'articles' in r:

            contents  =  r['articles']
            array  =  []
            for i in contents:
                Rake  =  RAKE.Rake('stopwords_en.txt')  # takes stopwords as list of strings
                words  =  Rake.run(i['title'])
                tagWordArray  =  []
                for word in words:
                    tagWordArray.append(word[0].title())
                itemArray  =  dict()
                itemArray['title']  =  i['title']
                itemArray['author']  =  i['author']
                itemArray['description']  =  i['description']
                itemArray['url']  =  i['url']
                itemArray['urlToImage']  =  i['urlToImage']
                itemArray['publishedAt']  =  i['publishedAt']
                itemArray['tags']  =  tagWordArray
                itemArray['created_at']  =  str(datetime.now())
                itemArray['source']  =  self.source
                itemArray['category']  =  self.category
                itemArray['type']  =  self.type
                # m  =  hashlib.md5()
                # m.update(i['title'])
                itemArray['uTag']  =  hashlib.sha256(str(i['title']).encode('utf-8')).hexdigest()[:16]



                array.append(itemArray)

            insert  =  db.tempMain.insert_many(array).inserted_ids
            if insert:
                logger.info('Inserted for ' + self.source + ' of type '
                            + self.type + str(datetime.now()))
                logging.info('\n')

            else:

                logger.warning('Error in insertion for ' + self.source
                            + ' of type ' + self.type
                            + str(datetime.now()))
                logging.warning('\n')



# URL classifying class

class primaryUrlClass:

    def __init__(
        self,
        url,
        name,
        category,
        ):
        self.url  =  url
        self.name  =  name
        self.category  =  category

    def callScrapping(self):

        url  =  self.url + 'top&apiKey = ' + api_key
        ApiCallTop  =  scrapping(url, self.name, self.category, 'top')
        ApiCallTopResponse  =  ApiCallTop.call_url()



        url  =  self.url + 'latest&apiKey = ' + api_key
        ApiCallLatest  =  scrapping(url, self.name, self.category,
                                  'latest')
        ApiCallLatestRes  =  ApiCallLatest.call_url()


        url  =  self.url + 'popular&apiKey = ' + api_key
        ApiCallpopular  =  scrapping(url, self.name, self.category,
                                   'popular')
        ApiCallpopularResponse  =  ApiCallpopular.call_url()



#db1.gobuzz.mobi
class allocation:

    def __init__(self, name):
        self.name = name

    def allocation_fun(self):
        for doc in db.tempMain.find({}):
            if str(doc['category'])  ==  "General":
                if not db.generalMain.find({"uTag":str(doc['uTag'])}).count() > 0:
                    for document in db.generalMain.find():
                        collision=fuzz.token_sort_ratio(str(doc['title']),document['title'] )
                        print(collision)
                        if int(collision) <  50:
                            insertDoc = db.generalMain.insert_one(doc)
                            if insertDoc:
                                logging.info('Insert new for general')
                                logging.info('\n')
                            else:
                                logging.info('Error in insertion for general')
                                logging.info('\n')



                        print(document['title'])
                        print("\n")


                    # insertDoc = db.generalMain.insert_one(doc)
                    # if insertDoc:
                    #     logging.info('Insert new for general')
                    #     logging.info('\n')
                    # else:
                    #     logging.info('Error in insertion for general')
                    #     logging.info('\n')
            elif str(doc['category'])  ==  "Technology":
                if not db.techMain.find({"uTag":str(doc['uTag'])}).count() > 0:
                    insertDoc = db.techMain.insert_one(doc)
                    if insertDoc:
                        logging.info('Insert new for Technology')
                        logging.info('\n')
                    else:
                        logging.info('Error in insertion for Technology')
                        logging.info('\n')




            else:
                print("Nothing")


        # remove = db.tempMain.remove()









def main():

    allocationCall = allocation("Hi");
    print(allocationCall.allocation_fun())
    return "j"




    primeURLCallCNN  =  \
        primaryUrlClass('https://newsapi.org/v1/articles?source = cnn&sortBy = '
                        , 'CNN', 'General')
    primeURLCallCNN.callScrapping()



    primeURLCallNextWeb  =  \
        primaryUrlClass(' https://newsapi.org/v1/articles?source = the-next-web&sortBy = '
                        , 'The Next Web', 'Technology')
    primeURLCallNextWeb.callScrapping()



    primeURLCallBBC  =  \
        primaryUrlClass(' https://newsapi.org/v1/articles?source = bbc-news&sortBy = '
                        , 'BBC-News', 'General')
    primeURLCallBBC.callScrapping()



    allocationCall = allocation("Hi");
    print(allocationCall.allocation_fun())

    return "ih"





if __name__  ==  '__main__':
    main()
