from common.database import Database
from common.scraper import Scraper
from models.book import Book
from flask import Flask, render_template, request, session, make_response
from dotenv import load_dotenv

scrape = False
debug = False
load_dotenv()


def create_app():
    app = Flask(__name__)  # '__main__'
    app.secret_key = "paris"

    @app.route('/', methods=['POST', 'GET'])
    def home():
        if request.method == 'GET':
            return render_template('home.html')
        else:
            ingredients = request.form['ingredients']
            your_book = Book.from_ingredients(ingredients=ingredients)
            return make_response(recipe_book(your_book.recipes))

    @app.route('/recipe_book', methods=['POST', 'GET'])
    def recipe_book(your_book):
        return render_template('book.html', your_book=your_book)

    @app.before_first_request
    def initialize_database():
        Database.initialize()
    return app


def run_scraping():
    Database.initialize()
    scrape1 = Scraper()
    scrape1.scrape_urls()
    scrape1.urls_from_DB()
    scrape1.metadata_scraper()
    Database.create_index()


if scrape:
    run_scraping()
if debug:
    app1 = create_app()
    if __name__ == '__main__':
        app1.run(port=4995, debug=True)




