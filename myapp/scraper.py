from bs4 import BeautifulSoup
import requests
import re


def scrapper(app):
    base = "https://play.google.com/store/apps/details?id="
    req = requests.get(base + app)
    soup = BeautifulSoup(req.content, "html.parser")
    # "applicationCategory":
    matches = soup.find(text=re.compile('"applicationCategory":'))
    stringy = str(matches)
    categories = ["Art", "Auto", "Beauty", "Books", "Business", "Comics", "Communications", "Dating", "Education",
                  "Entertainment",
                  "Events", "Finance", "Food", "Health", "House", "Libraries", "Lifestyle", "Maps", "Medical", "Music",
                  "News", "Parenting",
                  "Personalization", "Photography", "Productivity", "Shopping", "Social", "Sports", "Tools", "Travel",
                  "Video",
                  "Players", "Weather"]
    fcatgories = ["Art & Design", "Auto & Vehicles", "Beauty", "Books & Reference", "Business", "Comics",
                  "Communication",
                  "Dating", "Education", "Entertainment", 'Events', "Finance", 'Food & Drink', 'Health & Fitness',
                  'House & Home', 'Libraries & Demo', 'Lifestyle', 'Maps & Navigation', 'Medical', 'Music & Audio',
                  'News & Magazines', 'Parenting', 'Personalization', 'Photography', 'Productivity', 'Shopping',
                  'Social', 'Sports', 'Tools', 'Travel & Local', 'Video Players & Editors', 'Weather']
    count = 0
    for category in categories:
        if (category.upper() in stringy.upper()):
            return (fcatgories[count])
        count += 1
    if (count > 31):
        return ("Game")


def linkgen(name):
    base = "https://play.google.com/store/search?q="
    req = requests.get(base + name)
    soup = BeautifulSoup(req.content, "html.parser")
    soup2 = soup.find(class_="Si6A0c Gy4nib")
    idStr = soup2['href'].split('id=')[-1]

    return (idStr, scrapper(idStr))


# print(scrapper('com.elevatelabs.geonosis'))
# Si6A0c Gy4nib
