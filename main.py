from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import requests
import json


class scrapping:

   def __init__(self, url,tag):
      self.url = url
      self.tag = tag
   
   def call_url(self):
   	 headers = {"Accept": "application/json"}
   	 r=requests.get(self.url, headers=headers)
   	 contents=r.content
   	 return type(contents)



app=Flask(__name__)
app.config['MONGO_DBNAME'] = 'Culminate'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Culminate'

mongo=PyMongo(app)


@app.route('/', methods=['GET'])
def first_route():
	   prime_call= scrapping("https://newsapi.org/v1/articles?source=cnn&sortBy=top&apiKey=e428fe12b6ea434ca78b3c3d3e705c15", "BBC")
	   prime_call_response=prime_call.call_url()
	   return prime_call_response




if __name__ == '__main__':
    app.run(debug=True)


