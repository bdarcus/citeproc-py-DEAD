# would prefer to use cElementTree here for speed and memory, but 
# a) there seems to be a parsing bug, and b) CSL files are small
from xml.etree.ElementTree import ElementTree
import json

CSLNS = '{http://purl.org/net/xbiblio/csl}'

# >>> classes <<<

class Style(ElementTree):
    """
    An ElementTree wrapper to easily parse and work with a CSL instance.
    """

    def __init__(self, csl_fname):
        _style = self.parse(csl_fname)
        _info = _style.find(CSLNS + 'info')
        self.title = _info.find(CSLNS + 'title').text
        self.updated = _info.find(CSLNS + 'updated').text
        self.macros = _style.findall(CSLNS + 'macro')
        self.citation = _style.find(CSLNS + 'citation')
        self.bibliography = _style.find(CSLNS + 'bibliography')
        
        if self.citation:
            self.citation.layout = self.citation.find('{http://purl.org/net/xbiblio/csl}layout')
            self.citation.options = self.citation.findall('{http://purl.org/net/xbiblio/csl}option')

        if self.bibliography:
            self.bibliography.options = self.bibliography.find('{http://purl.org/net/xbiblio/csl}option')
            self.bibliography.layout = self.bibliography.find('{http://purl.org/net/xbiblio/csl}layout')

    def get_macro(name):
        pass



class FormattedNode:
    """
    The formatted output.
    """
    def __init__(self, field, content, style=None, prefix=None, suffix=None, 
                 quote=False, block=False, href=None):
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

# >>> processing functions <<<

def sortkey(reference, style, context='bibliography'):
    """
    When given a Reference and a Style, returns a sorting key.
    """
    return(reference['title'], reference['date'])

def process_group(node, item):
    pass

def process_names(node, item):
    pass

def process_choose(node, item):
    pass

def process_text(node, item):
    fstyle = node.get('font-style')
    fweight = node.get('font-weight')
    fvariant = node.get('font-variant')
    prefix = node.get('prefix')
    suffix = node.get('suffix')
    variable = node.get('variable')
    content = item[node.get('variable')] if variable in item else None
    formatted_node = FormattedNode(field=variable, content=content)
    return(formatted_node)

def process_node(node, item):
    """
    """
    if node.tag == CSLNS + "group":
        process_group(node, item)
    elif node.tag == CSLNS + "names":
        process_names(node, item)
    elif node.tag == CSLNS + "choose":
        process_choose(node, item)
    elif node.tag == CSLNS + "text":
        return(process_text(node, item))

def process_citation(style, reference_list, citation, mode='html'):
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

def add_year_suffix(reference_list):
    """
    Given the list of References, compare year and contributors' names and, 
    when they collide, generate a suffix to append to the year for 
    disambiguation.
    """
    pass
