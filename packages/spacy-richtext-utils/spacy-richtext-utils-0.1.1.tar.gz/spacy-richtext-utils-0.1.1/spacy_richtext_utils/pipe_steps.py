from spacy import Language
from spacy.tokens import Span


@Language.component("iter_spans")
def ents_and_toks(doc):
    doc._.spans = IterSpans(doc)
    return doc


@Language.component("html_ents_enricher")
def html_ents_enricher(doc):
    entities = list(doc.ents)
    new_ents = []

    cur_html_id = False
    for tok in doc:
        if tok._.html_tag_id == cur_html_id and cur_html_id is not False:
            new_ents[-1].append(tok)
        else:
            cur_html_id = tok._.html_tag_id
            if cur_html_id != False:
                new_ents.append([tok])

    new_spans = [
        Span(doc, ent[0].i, ent[-1].i + 1, 'RICHTXT')
        for ent in new_ents
    ]

    doc.ents = entities + new_spans

    return doc


class IterSpans:
    def __init__(self, doc):
        self.doc = doc
        for ent in doc.ents:
            for tok in ent:
                tok._.entity = ent

    def __iter__(self):
        self.tok_it = iter(self.doc)
        return self

    def __next__(self):
        while True:
            tok_or_ent = next(self.tok_it)
            if tok_or_ent.ent_iob_ != 'I': break

        if tok_or_ent.ent_iob_ == 'B':
            return tok_or_ent._.entity

        return tok_or_ent
