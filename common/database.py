import pymongo


class Database:
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['recipeDB']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query, field=None):
        return Database.DATABASE[collection].find(query, field)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update_one(collection, query, data):
        return Database.DATABASE[collection].update_one(query, {"$set": data})
        myquery = {"address": "Valley 345"}
        newvalues = {"$set": {"address": "Canyon 123"}}

        mycol.update_one(myquery, newvalues)