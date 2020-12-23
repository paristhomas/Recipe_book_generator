from models.recipe import Recipe
from common.database import Database
from common.scraper import Scraper


Database.initialize()

scrape1 = Scraper()
scrape1.run_scraper()
scrape1.urls_from_DB()
scrape1.metadata_scraper()



