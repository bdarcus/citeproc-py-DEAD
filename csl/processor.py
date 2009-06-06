

class FormattedNode:
    """
    The formatted output.
    """
    def __init__(self, field, content, style=None, prefix=None, suffix=None, block=False, href=None):
        self.field = field
        self.content = content
        self.style = style
        self.prefix = prefix
        self.suffix = suffix
        self.block = block

    def to_html(rdfa=False):
        result = ""
        result += self.prefix
        result += self.content
        result += self.suffix
        return(result)



class FormattedList:
    """
    The formatted output.
    """
    def __init__(self, items, delimiter=None, prefix=None, suffix=None, block=False):
        self.items = items
        self.prefix = prefix
        self.suffix = suffix
        self.block = block



class FormattedCitationCluster(FormattedList):
    pass



class FormattedReferenceList(FormattedList):
    pass



def process_citations(style, reference_list, citation):
    """
    With a Style, a list of References and the list of citation groups 
    (the list of citations with their locator), produce the FormattedOutput 
    for each citation group.
    """
    pass



def process_bibliography(style, reference_list):
    """
    With a Style and the list of References produce the FormattedOutput 
    for the bibliography.  
    """
    pass



def citeproc(style, reference_list):
    """
    With a Style, a list of References and the list of citation 
    groups (the list of citations with their locator), produce the 
    FormattedOutput for each citation group and the bibliography.
    """
    pass



def proc_biblio(style, reference_list):
    """
    With a Style and a sorted list of References produce the evaluated 
    output for the bibliography.
    """
    pass



def proc_refs(style, reference_list):
    """
    Given the CSL Style and the list of References sort the list according 
    to the Style and assign the citation number to each Reference.
    """
    pass


def refs_year_suffix(reference_list):
    """
    Given the list of References, compare year and contributors' names and, 
    when they collide, generate a suffix to append to the year for 
    disambiguation.
    """
    pass

