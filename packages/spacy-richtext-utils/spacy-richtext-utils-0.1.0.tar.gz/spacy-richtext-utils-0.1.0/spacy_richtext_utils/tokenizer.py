from bs4 import BeautifulSoup


class HTMLRichTokenizer():

    def __init__(self, tokenizer):

        self.tokenizer = tokenizer

        self.tag_as_ent = [
            'span', 'a', 'b', 'strong', 'i', 'title', # inline tags
            'li', 'td', 'th', # table and list elements
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6' # headers
        ]
        self.maxlen_for_ent = 40
        self.minlen_for_ent = 3

    def __call__(self, string):
        soup = BeautifulSoup(string, features="html.parser")
        doc = self.tokenizer(soup.text)

        html_it = iter(soup.strings)
        soupstr_pos = 0
        tag = None
        tag_gr = 0
        for tok in doc:

            while tok.idx >= soupstr_pos:
                tag = next(html_it)
                soupstr_pos += len(tag.text)
                tag_gr += 1

            if tag is not None and tag.parent is not None \
                    and tag.parent.name in self.tag_as_ent \
                    and self.minlen_for_ent < len(tag.text) < self.maxlen_for_ent:
                tok._.html_tag_id = tag_gr

        return doc