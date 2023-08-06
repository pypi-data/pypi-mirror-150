from spacy.tokens import Doc, Token, Span
from . import HTMLRichTokenizer

def html_utils(nlp):
    Token.set_extension("html_tag_id", default=False, force=True)
    Token.set_extension("entity", default=None, force=True)
    Doc.set_extension("spans", default=False, force=True)

    nlp.tokenizer = HTMLRichTokenizer(nlp.tokenizer)
    nlp.add_pipe("html_ents_enricher", first=True)
    nlp.add_pipe("iter_spans", last=True)

    return nlp








