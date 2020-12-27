from models.recipe import Recipe
from common.database import Database

class Book(object):
    def __init__(self, recipes, ingredients=None):
        self.recipes = recipes
        self.Ingredients = ingredients

    def length(self):
        return len(self.recipes)

    @classmethod
    def from_ingredients(cls, ingredients):
        ingredients_list = ingredients.split(" ")
        urls = Book.ingredients2recipes(ingredients)
        #rank results
        recipes = []
        for url in urls:
            recipes.append(Recipe.initilizeFromMongo(url=url["URL"]))
        return cls(recipes, ingredients_list)

    @staticmethod
    def ingredients2recipes(ingredients, limit=50):
        #query = {"Name":{"$regex": ".*"+ ingredients[0] +".*",
         #                "$options" :'i' }}
        #db.test.aggregate([{$match: { $text: { $search: terms}}},{$project: {_id: 0, Name: 1, "URL": 1, Ingredients: 1, score: {$let: {vars: {matches: {$meta: "textScore"}, noOfIngredients: {$size: "$Ingredients"}},in: { $divide: [ "$$matches", "$$noOfIngredients" ]}}}}},{ $sort: {score: -1}}])
        query = [{"$match": { "$text": { "$search": ingredients}}},
                 {"$project": {"_id": 0,
                               "Name": 1,
                               "URL": 1,
                               "Ingredients": 1,
                               "score": {"$let": {"vars": {"matches": {"$meta": "textScore"},
                                                           "noOfIngredients": {"$size": "$Ingredients"}},
                                                  "in": {"$divide": ["$$matches", "$$noOfIngredients"]}}}}},
                 {"$sort": {"score": -1}},
                 {"$limit": limit},
                 ]
        urlList = Database.aggregate(query=query)
        return urlList
