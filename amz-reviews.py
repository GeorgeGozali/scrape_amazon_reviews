import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.amazon.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/product-reviews\
    /B07P4LSDYV/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={}"
reviewlist = []


def get_soup(url):
    # you need splash server running on you machine
    r = requests.get(
        "http://localhost:8050/render.html",
        params={"url": url, "wait": 2}
    )

    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def get_reviews(soup):
    reviews = soup.find_all("div", {"data-hook": "review"})
    try:
        for item in reviews:
            review = {
                "product": soup.title.text.replace("Amazon.com: Customer reviews:", "").strip(),
                "title": item.find("a", {"data-hook": "review-title"}).text.strip(),
                # "rating": item.find("span", class_="a-icon-alt").text.split()[0],
                "rating": float(item.find("i", {"data-hook": "review-star-rating"}).text.replace("out of 5 stars", "").strip()),
                "body": item.find("span", {"data-hook": "review-body"}).text.strip()
            }
            reviewlist.append(review)
    except Exception as e:
        print(e)


for x in range(1, 999):
    soup = get_soup(url.format(x))
    print(f"Getting page: {x}")
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find("li", {"class": "a-disabled a-last"}):
        pass
    else:
        break

df = pd.DataFrame(reviewlist)
df.to_excel("rpi3b+-reviews.xlsx", index=False)
print("Fin.")
