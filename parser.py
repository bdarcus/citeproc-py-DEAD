from pyparsing import *

key = Word(alphanums)

citation = "[" + delimitedList(key, ';') + "]"

doc = "One [doe99] two [smith09; jones08]. Three [zon05]."

for c in citation.searchString(doc):
    print c


