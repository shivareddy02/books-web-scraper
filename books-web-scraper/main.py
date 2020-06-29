
import requests
import re
from bs4 import BeautifulSoup
from time import sleep
from csv import DictWriter

BASE_URL = "http://books.toscrape.com/catalogue/"
all_books = []
url = "page-1.html"


while url:
    response = requests.get(BASE_URL + url)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all(class_ = "product_pod")
    for book in books:
        all_books.append({
        "book" : book.find('h3').findChild().get('title','No title attribute'),
        "price": re.sub("Â","",book.find(class_ = "price_color").text),
        "stock": re.sub("\n","",(book.find(class_ = "instock availability").text).strip()),
        "rating": book.find(class_= "star-rating").get("class")[1]
        })
        nxt_btn = soup.find(class_ = "next")
        url = nxt_btn.find('a')['href'] if nxt_btn else None

#print(all_books)

with open("books.csv", "a", encoding="utf-8") as csv_file:
    headers = ["book", "price","stock","rating"]
    csv_writer = DictWriter(csv_file, fieldnames=headers)
    csv_writer.writeheader()
    for book in all_books:
        csv_writer.writerow(book)

