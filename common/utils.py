from models.recipe import Recipe
class Utils:

    @staticmethod
    def url2mongo(_URL):
        foo = Recipe(method="URL", URL=_URL)
        foo.save2mongo()