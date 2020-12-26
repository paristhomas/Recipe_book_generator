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
        ingredients_list = ingredients.split(",")
        urls = Book.ingredients2recipes(ingredients_list)
        #rank results
        recipes = []
        for url in urls:
            recipes.append(Recipe.initilizeFromMongo(url=url["URL"]))
        return cls(recipes, ingredients_list)

    @staticmethod
    def ingredients2recipes(ingredients):
        query = {"Name":{"$regex": ".*"+ ingredients[0] +".*",
                         "$options" :'i' }}
        urlList = Database.find(query=query,
                      field={"URL": 1})
        return urlList
