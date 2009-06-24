
from style import NS_CSL


class FormattedNode:
    """
    The formatted output.
    """
    def __init__(self, field, content, style=None, prefix=None, suffix=None, quote=False, block=False, href=None):
        self.field = field
        self.content = content
        self.style = style
        self.prefix = prefix
        self.suffix = suffix
        self.block = block
        self.quote = quote

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



def sortkey(reference, style, context='bibliography'):
    """
    When given a Reference and a Style, returns a sorting key.
    """
    return(reference['title'], reference['date'])


def process_group(node):
    pass


def process_names(node):
    pass


def process_choose(node):
    pass


def process_text(node):
    return(FormattedNode())


def process_node(node, item):
    """
    """
    if node.tag == NS_CSL + "group":
        process_group(node)
    elif node.tag == NS_CSL + "names":
        process_names(node)
    elif node.tag == NS_CSL + "choose":
        process_choose(node)
    else:
        process_text(node)


def process_nodes(nodes):
    for element in nodes.iter():
        process_node(element)


def process_citations(style, reference_list, citation, mode='html'):
    """
    With a Style, a list of References and the list of citation groups 
    (the list of citations with their locator), produce the for 
    FormattedOutput each citation group.
    """
    formatted_citation = [[process_node(node, citeref) for node in style.citation.layout] 
                             for citeref in citation]

    return(formatted_citation)


def process_bibliography(style, reference_list):
    """
    With a Style and the list of References produce the FormattedOutput 
    for the bibliography.  
    """
    formatted_list = [[process_node(node, item) for node in style.bibliography.layout] 
                         for item in reference_list]

    return(formatted_list)


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

