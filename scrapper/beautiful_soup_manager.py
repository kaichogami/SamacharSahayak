from typing import List

import requests
from bs4.element import Tag

from bs4 import BeautifulSoup

class BeautifulSoupManager:

    def __init__(self, url: str):
        page = requests.get(url).text
        self.soup = BeautifulSoup(page, "html.parser")

    def find_by_tag(self, tag: str, attrs: dict) -> Tag:
        return self.soup.find(tag, attrs)

    def get_all_links_in_bs4_tag(self, bs4_tag: Tag) -> List[str]:
        links_list = list()
        for a in bs4_tag.find_all('a', href=True):
            links_list.append(a['href'])
        return links_list
