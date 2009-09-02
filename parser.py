from pyparsing import *

DOC = "One [doe99] two [smith09; jones08]. Three [zon05@23]."

CITED = []

def parse_citations(document):
    lbracket = Suppress("[")
    rbracket = Suppress("]")
    digits = "0123456789"
    key = Group(Word(alphanums) + Optional(Suppress("@")) + Optional(Word(digits)))
    citation = lbracket + delimitedList(key, ";") + rbracket

    return(citation.searchString(document))

print parse_citations(DOC)


