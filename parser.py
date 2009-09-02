from pyparsing import *

DOC = "One [doe99] two [smith09; jones08]. Three [zon05]."

def parse_citations(document):
    lbracket = Suppress( "[" )
    rbracket = Suppress( "]" )

    key = Word(alphanums)

    citation = lbracket + delimitedList(key, ';') + rbracket

    return(citation.searchString(document))

print parse_citations(DOC)


