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
        soup = self.html_2_soup(html)

        def img_tag(tag):
            return tag.name == "img" and tag.has_attr('class') and tag.attrs["class"][0] == "wp-manga-chapter-img"

        img_tags = soup.find_all(img_tag)
        return img_tags

    def get_chapters_list(self,html) -> list:
        """get chapters docs list for mongo"""
        chaps = self.parse_chapters(html)
        docs = []
        for ind,c in enumerate(chaps[::-1]):
            doc = {"url":c.attrs["href"],
                   "name":c.string.strip(),
                   "index":ind
            }
            docs.append(doc)
        return docs
    def get_images_list(self,html) -> list:
        """get images docs list for mongo"""
        images = self.parse_images(html)
        docs = []
        for ind, c in enumerate(images):
            doc = {"url": c.attrs["src"].strip(),
                   "index": ind
                   }
            docs.append(doc)
        return docs

ParserMAP = {
    1: ManhwaWorldParser
}
