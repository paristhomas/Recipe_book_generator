import uuid
import requests
import dateparser
from datetime import timedelta
from bs4 import BeautifulSoup
from common.database import Database



class Recipe:
    def __init__(self, URL=None, _id=None, Name=None, Ratings=None, Cooktime=None, Effort=None, Ingredients=None, method="URL"):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.URL = URL
        self.Name = Name
        self.Ratings = Ratings
        self.Cooktime = Cooktime
        self.Effort = Effort
        self.Ingredients = Ingredients
        if method == "URL" and URL is not None:
            if self.fromMongo() is None:
                self.save2mongo()
        if method == "DB":
            self.fromMongo()

    def update_from_url(self):
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
        dt = timedelta(0)
        try:
            sub_Element = element.find_all("time")
            for subsubElement in sub_Element:
                time = subsubElement.text
                t = dateparser.parse("now") - dateparser.parse(time)
                dt += t
        except: pass
        self.Cooktime = round(dt.seconds / 60, 0)

        # Effort
        TAG_NAME = "div"
        QUERY = "icon-with-text masthead__skill-level body-copy-small body-copy-bold icon-with-text--aligned"
        element = soup.find(TAG_NAME, QUERY)
        try: self.Effort = element.text
        except: self.Effort = None

        # Ingredients
        TAG_NAME = "section"
        QUERY = "recipe-template__ingredients col-12 mt-md col-lg-6"
        element = soup.find(TAG_NAME, QUERY)
        sub_Element = element.find_all("li")
        Ingredients = []
        for subSubElement in sub_Element:
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
        Database.insert(data=self.json())
    def updateMongoReciepe(self):
        Database.update_one(query= {"URL": self.URL},
                            data=self.json())
        return self.json()

    def fromMongo(self):
        return Database.find_one(query={"URL": self.URL})

    @classmethod
    def initilizeFromMongo(cls, url):
        result = Database.find_one(query={"URL": url})
        return cls(**result)


