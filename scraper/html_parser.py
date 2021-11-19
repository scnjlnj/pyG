from bs4 import BeautifulSoup


class BaseParser(object):
    pass


class ManhwaWorldParser(BaseParser):
    """parser for https://manhwaworld.com html"""
    def html_2_soup(self,html):
        return BeautifulSoup(html,parser="html.parser",features="lxml")

    def parse_chapters(self, html) -> list:
        """get chapters urls on chapter list page"""
        soup = self.html_2_soup(html)
        def chapter_a_tag(tag):
            return tag.name == "a" and hasattr(tag, "parent") and tag.parent.has_attr('class') and \
                   tag.parent.attrs["class"][0] == "wp-manga-chapter"

        chapters_a = soup.find_all(chapter_a_tag)
        return chapters_a

    def parse_images(self, html) -> list:
        """get image urls on detail page"""
        pass

    def get_chapters_list(self,html) -> list:
        """get images docs list for mongo"""
        chaps = self.parse_chapters(html)
        docs = []
        for ind,c in enumerate(chaps[::-1]):
            doc = {"url":c.attrs["href"],
                   "name":c.name.strip(""),
                   "index":ind
            }
            docs.append(doc)
        return docs
    def get_images_list(self,html) -> list:
        """get images docs list for mongo"""
        pass

ParserMAP = {
    1: ManhwaWorldParser
}
