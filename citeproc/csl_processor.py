
process_citations(style, reference_list, citation):
"""
With a Style, a list of References and the list of citation groups (the list of citations with their locator), produce the FormattedOutput for each citation group.
"""


process_bibliography(style, reference_list):
"""
With a Style and the list of References produce the FormattedOutput for the bibliography.
"""


citeproc :: Style -> [Reference] -> [[(String, String)]] -> BiblioData
"""
With a Style, a list of References and the list of citation groups (the list of citations with their locator), produce the FormattedOutput for each citation group and the bibliography.
"""

proc_biblio(style, reference_list):
"""
With a Style and a sorted list of References produce the evaluated output for the bibliography.
"""


proc_refs(style, reference_list):
"""
Given the CSL Style and the list of References sort the list according to the Style and assign the citation number to each Reference.
"""


refs_year_suffix(reference_list):
"""
Given the list of References, compare year and contributors' names and, when they collide, generate a suffix to append to the year for disambiguation.
"""

