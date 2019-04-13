
class ScrappedLinkStructure:
    def __init__(self, heading: str, link: str):
        self.heading = heading
        self.link = link


class ScrappedArticle:
    def __init__(self, title: str, html_data: str):
        self.title = title
        self.html_data = html_data


class FormattedArticle:
    def __init__(self, title: str, scrapped_articles_html: str):
        self.heading = title
        self.scrapped_articles_html = scrapped_articles_html