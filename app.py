import requests
import dateparser
from datetime import timedelta
from bs4 import BeautifulSoup


URL = 'https://www.bbcgoodfood.com/recipes/chilli-con-carne-recipe'
response = requests.get(URL)
content = response.content
soup = BeautifulSoup(content, "html.parser")

# data to extract:
# Name of dish
TAG_NAME = "h1"
QUERY = "masthead__title heading-1"
element = soup.find(TAG_NAME, QUERY)
nameOfDish = element.text
print(nameOfDish)
# Number of ratings
TAG_NAME = "span"
QUERY = "rating__count-text body-copy-small"
element = soup.find(TAG_NAME, QUERY)
numRatings = int("".join(filter(str.isdigit, element.text)))
print(numRatings)
# Time
TAG_NAME = "div"
QUERY = "icon-with-text time-range-list cook-and-prep-time masthead__cook-and-prep-time"
element = soup.find(TAG_NAME, QUERY)
subElement = element.find_all("time")
dt = timedelta(0)
for subsubElement in subElement:
    time = subsubElement.text
    t = dateparser.parse("now") - dateparser.parse(time)
    dt += t
cooktime = round(dt.seconds/60,0)
# Effort
TAG_NAME = "div"
QUERY = "icon-with-text masthead__skill-level body-copy-small body-copy-bold icon-with-text--aligned"
element = soup.find(TAG_NAME, QUERY)
print(element.text)
# Ingredients
TAG_NAME = "section"
QUERY = "recipe-template__ingredients col-12 mt-md col-lg-6"
element = soup.find(TAG_NAME, QUERY)
subElement = element.find_all("li")
Ingredients = []
for subSubElement in subElement:
    Ingredients.append(subSubElement.text)
print(Ingredients)
