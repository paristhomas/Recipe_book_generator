import requests
import dateparser
from datetime import timedelta
from bs4 import BeautifulSoup
from common.database import Database


class Recipe:
    def __init__(self, URL=None, method="URL"):
        self.URL = URL
        self.Name = None
        self.Ratings = None
        self.Cooktime = None
        self.Effort = None
        self.Ingredients = None
        if method == "URL" and URL is not None:
            self.url2self()
        if method == "DB":
            pass

    def url2self(self):
        #@@ this should be setup better
        response = requests.get(self.URL)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        #name
        TAG_NAME = "h1"
        QUERY = "masthead__title heading-1"
        self.Name = soup.find(TAG_NAME, QUERY).text

        # Number of ratings
        TAG_NAME = "span"
        QUERY = "rating__count-text body-copy-small"
        element = soup.find(TAG_NAME, QUERY)
        self.Ratings = int("".join(filter(str.isdigit, element.text)))

        # Cook Time
        TAG_NAME = "div"
        QUERY = "icon-with-text time-range-list cook-and-prep-time masthead__cook-and-prep-time"
        element = soup.find(TAG_NAME, QUERY)
        subElement = element.find_all("time")
        dt = timedelta(0)
        for subsubElement in subElement:
            time = subsubElement.text
            t = dateparser.parse("now") - dateparser.parse(time)
            dt += t
        self.Cooktime = round(dt.seconds / 60, 0)

        # Effort
        TAG_NAME = "div"
        QUERY = "icon-with-text masthead__skill-level body-copy-small body-copy-bold icon-with-text--aligned"
        element = soup.find(TAG_NAME, QUERY)
        self.Effort = element.text

        # Ingredients
        TAG_NAME = "section"
        QUERY = "recipe-template__ingredients col-12 mt-md col-lg-6"
        element = soup.find(TAG_NAME, QUERY)
        subElement = element.find_all("li")
        Ingredients = []
        for subSubElement in subElement:
            Ingredients.append(subSubElement.text)
        self.Ingredients = Ingredients
        return

    def json(self):
        return {"URL": self.URL,
                "Name": self.Name,
                "Ratings": self.Ratings,
                "Cooktime": self.Cooktime ,
                "Effort": self.Effort,
                "Ingredients": self.Ingredients
                }

    def save2mongo(self):
        Database.insert(collection="recipes",
                        data=self.json())



