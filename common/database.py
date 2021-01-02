import os
import pymongo


class Database:
    URI = os.environ.get("MONGO_URI")
    DATABASE = None
    global_collection = "test"

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["recipeDB"]

    @staticmethod
    def insert(data, collection=global_collection):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(query, field=None, collection=global_collection):
        return Database.DATABASE[collection].find(query, field)

    @staticmethod
    def find_one(query, collection=global_collection):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update_one(query, data, collection=global_collection):
        return Database.DATABASE[collection].update_one(query, {"$set": data})

    @staticmethod
    def aggregate(query, collection=global_collection):
        return Database.DATABASE[collection].aggregate(query)

    @staticmethod
    def create_index(index="Ingredients", collection=global_collection):
        Database.DATABASE[collection].drop_index("text")
        return Database.DATABASE[collection].create_index([(index, pymongo.TEXT)], name='text')
