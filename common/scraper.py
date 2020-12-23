import requests
from models.recipe import Recipe
from bs4 import BeautifulSoup
from common.database import Database

class Scraper:
    def __init__(self):
        self.url_list = []
    #https://www.bbcgoodfood.com/search/recipes/page/416/?sort=-date

    def scrape_urls(self):
        urlstart = "https://www.bbcgoodfood.com/search/recipes/page/"
        urlend = "/?sort=-date"
        for pagenum in range(1,500):
            URL = urlstart + str(pagenum) + urlend
            response = requests.get(URL)
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            TAG_NAME = "div"
            QUERY = "template-search-universal__main template-search-universal__main--list"
            element = soup.find(TAG_NAME, QUERY)
            subElement = element.find_all("h4")
            for subSubElement in subElement:
                foo = subSubElement.find("a")
                self.url_list.append("https://www.bbcgoodfood.com/" + str(foo.get('href')))
            print(pagenum)

    def run_scraper(self):
        self.scrape_urls()
        for url in self.url_list:
             foo = Recipe(URL=url, method="URL")
             foo.url2self()
             foo.save2mongo()
             print(foo.Name)


