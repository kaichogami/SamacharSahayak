import datetime
import re
import pytz
import datetime
from typing import List

from bs4.element import Tag
from scrapper.beautiful_soup_manager import BeautifulSoupManager
from scrapper.constants import ScrappedLinkStructure, ScrappedArticle, FormattedArticle

SECTION_TO_READ = {"National": "https://www.thehindu.com/todays-paper/tp-national/",
                   "International": "https://www.thehindu.com/todays-paper/tp-international/",
                   "Business": "https://www.thehindu.com/todays-paper/tp-business/",
                   "Opinion": "https://www.thehindu.com/todays-paper/tp-opinion/"}

class TheHinduScrapper:

    def __init__(self, date: str):
        """
        date: A string for which date scrapper should scrap for. Format: yyyy/mm/dd
        """
        self.url = "https://www.thehindu.com/archive/print/{}/".format(date)
        self.beautiful_soup_manager = BeautifulSoupManager(self.url)

    def get_all_sections(self) -> List[Tag]:
        section_tag_details_list = []
        section_number = 1
        section_tag_details = self.get_section_detail(section_number)
        while section_tag_details is not None:
            section_number += 1
            section_tag_details_list.append(section_tag_details)
            section_tag_details = self.get_section_detail(section_number)
        return section_tag_details_list

    def get_section_detail(self, section_number: str) -> Tag:
        return self.beautiful_soup_manager.find_by_tag("section", {"id":"section_{}".format(section_number)})

    def get_all_links(self) -> List[ScrappedLinkStructure]:
        all_content = list()
        all_sections = self.get_all_sections()
        for section in all_sections:
            for heading, concerned_section_link in SECTION_TO_READ.items():
                if section.find("a", attrs={"href": concerned_section_link}):
                   section_links = self.beautiful_soup_manager.get_all_links_in_bs4_tag(section)
                   section_links.remove(concerned_section_link)
                   for link in section_links:
                       all_content.append(ScrappedLinkStructure(heading, link))

        return all_content

    def get_scrapped_article(self, scrapped_link: ScrappedLinkStructure):
        bs = BeautifulSoupManager(scrapped_link.link)
        div_ids = re.findall(r"content-body-\d*-\d*", bs.soup.text)
        if not div_ids:
            return {"Coudln't scrap": "aaa"}

        title_group = bs.find_by_tag("h2", attrs={"class": "intro"})
        if title_group:
            title = title_group.text.strip("\n").replace('<div id="{}">'.format(div_ids[0]), '')
        else:
            title = "Title not Found"
        content = bs.find_by_tag("div", attrs={"id": div_ids[0]}).decode_contents()
        return ScrappedArticle(title, content).__dict__

    def get_formatted_data(self, heading, scrapped_article):
        return FormattedArticle(heading, scrapped_article).__dict__

    def convert_to_jinja_data(self, final_html_data):
        return {
            "all_news_data": final_html_data,
            "today_date": datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%Y")
        }

    def get_all_content(self) -> dict:
        final_html_data = {heading: [] for heading in SECTION_TO_READ.keys()}
        scrapped_links = self.get_all_links()
        for sl in scrapped_links:
            print("getting data for {}".format(sl.heading))
            scrapped_article = self.get_scrapped_article(sl)
            final_html_data[sl.heading].append(scrapped_article)

        return self.convert_to_jinja_data(final_html_data)


