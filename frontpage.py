import requests
from bs4 import BeautifulSoup


def get_and_cache(url, filename):
    try:
        with open(filename, "r") as f:
            data = f.read()
            return data
    except:
        data = requests.get(url).text
        f = open(filename, "w")
        f.write(data)
        f.close()
        return data

soup = BeautifulSoup(
    get_and_cache(
        "http://www.nytimes.com/pages/todayspaper/index.html",
        "frontpage.html"), "html.parser")

article_list = soup.find_all("div", {"class": "story"})


class Page(object):

    def __init__(self, title, author, summary, thumbnail):
        self.title = title
        self.author = author
        self.summary = summary
        self.thumbnail = thumbnail

    def set_url(self, url):
        self.url = url

    def __str__(self):
        return "Article title: {0}, author: {1}".format(
            self.title, self.author)

print(article_list[0].h3)
page_list = []

for article in article_list:
    title = article.h3
    title_text = title.text
    title_link = title.find("a")["href"]
    author = article.h6.text
    author = author[4:].replace(" and ", ", ")
    author = author.split(", ")
    author[-1] = author[-1].strip()
    summary = article.find("p", {"class": "summary"}).text
    thumbnail = article.find("img")["src"]
    temp_page = Page(title_text, author, summary, thumbnail)
    temp_page.set_url(title_link)
    page_list.append(temp_page)

for i in page_list:
    print(str(i))
