from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.cv04
collection = db.restaurants