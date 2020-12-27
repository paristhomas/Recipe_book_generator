from models.recipe import Recipe
from common.database import Database
from common.scraper import Scraper
from models.book import Book

from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)  # '__main__'
app.secret_key = "paris"


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        ingredients = request.form['ingredients']
        #standard_ingredients = request.form['standard_ingredients']
        your_book = Book.from_ingredients(ingredients=ingredients)
        return make_response(recipe_book(your_book.recipes))


@app.route('/recipe_book', methods=['POST', 'GET'])
def recipe_book(your_book):
    return render_template('book.html', your_book=your_book)


@app.before_first_request
def initialize_database():
    Database.initialize()


if __name__ == "__main__":
    app.run(debug=True)


"""
scrape1 = Scraper()
#scrape1.scrape_urls()
scrape1.urls_from_DB()
scrape1.metadata_scraper()
"""


