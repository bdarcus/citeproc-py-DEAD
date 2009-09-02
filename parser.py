from pyparsing import *

lbracket = Suppress( "[" )
rbracket = Suppress( "]" )

key = Word(alphanums)

citation = lbracket + delimitedList(key, ';') + rbracket

doc = "One [doe99] two [smith09; jones08]. Three [zon05]."

for c in citation.searchString(doc):
    print c


