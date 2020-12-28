import pymongo


class Database:
    URI = "mongodb+srv://paris1:qpgw67JxtAsD7b2@cluster0.c2oks.mongodb.net/Cluster0?retryWrites=true&w=majority"#"mongodb://127.0.0.1:27017"
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
