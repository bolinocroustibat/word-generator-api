import requests
from bs4 import BeautifulSoup


async def get_random_wikipedia_article(lang: str) -> str:
    text = ""
    url = requests.get(f"https://{lang}.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")
    article_soup = soup.find("div", class_="mw-parser-output")
    if article_soup:
        content_soup = article_soup.find_all(["h1", "h2", "p"], recursive=False)
        for s in content_soup:
            text += s.text
    return text.replace("\n", " ")
