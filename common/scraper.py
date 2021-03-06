import requests
from models.recipe import Recipe
from bs4 import BeautifulSoup
from common.database import Database


class Scraper:
    def __init__(self):
        self.url_list = []

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
                goo = str("https://www.bbcgoodfood.com" + str(foo.get('href')))
                self.url_list.append(goo)
                Recipe(URL=goo, method="URL")
            print(pagenum)

    def url_scraper(self):
        self.scrape_urls()
        for url in self.url_list:
            foo = Recipe(URL=url, method="URL")
            print(foo.Name)

    def metadata_scraper(self):
        for url in self.url_list:
            foo = Recipe(URL= url, method="DB")
            print(url)
            foo.update_from_url()
            print(foo.Name)
            foo.updateMongoReciepe()

    def urls_from_DB(self):
        urls = Database.find(query={},
                             field={"URL": 1, "Name": 1, "_id": 0})
        self.url_list = []
        for url in urls:
            if url["Name"] is None:
                self.url_list.append(url["URL"])
        return self.url_list
