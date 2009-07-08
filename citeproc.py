# would prefer to use cElementTree here for speed and memory, but 
# a) there seems to be a parsing bug, and b) CSL files are small
from xml.etree.ElementTree import Element, ElementTree
import json

CSLNS = '{http://purl.org/net/xbiblio/csl}'

# >>> classes <<<

class Style(ElementTree):
    """
    An ElementTree wrapper to easily parse and work with a CSL instance.
    >>> style = Style('some.csl')
    >>> style.title
    "Some Style"
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
    The formatted node, whose content is a string.
    """
    def __init__(self, variable, content, formatting=None):
        self.variable = variable
        self.content = content
        self.formatting = formatting

    def to_text(self):
        result = ""
        if 'prefix' in self.formatting:
            result += self.formatting['prefix']
        result += self.content
        if 'suffix' in self.formatting:
            result += self.formatting['suffix']
        return(result)



# >>> processing functions <<<

def sortkey(style, reference, context='bibliography'):
    """
    When give a Reference and a Style, returns a sorting key.
    """
    return(reference['title'], reference['date'])

def process_group(style_node, reference):
    """
    When given a style node and a reference, return an evaluated cs:group.
    """
    pass

def process_names(style_node, reference):
    """
    When given a style node and a reference, returns an evaluated list of 
    contributor names.
    """
    pass

def condition(condition_attributes, reference):
    """
    Evaluates a condition.
    """
    conditions = []

    if 'variable' in condition_attributes:
        variables = condition_attributes['variable'].split(" ")
        for variable in variables:
            conditions.append(variable in reference)

    if 'type' in condition_attributes:
        reftypes = condition_attributes['type'].split(" ")
        for reftype in reftypes:
            conditions.append(reftype == reference['type'])

    if 'match' in condition_attributes:
        match = condition_attributes['match']
        if match == 'none':
            return(True not in conditions)
        elif match == 'all':
            return(False not in conditions)
    else:
        return(True in conditions)

def process_choose(style_node, reference):
    """
    When given a style node and a reference, return an evaluated cs:choose.
    """
    pass

def process_text(style_node, reference):
    """
    When given a style node and a reference, return an evaludated cs:text.
    """
    formatting = style_node.attrib
    variable = style_node.get('variable')
    content = reference[style_node.get('variable')] if variable in reference else None

    if content:
        formatted_node = FormattedNode(variable=variable, content=content, formatting=formatting)
        return(formatted_node)
    else:
        pass

def process_node(style_node, reference):
    """
    Passes of style node processing to appropriate function.
    """
    if style_node.tag == CSLNS + "group":
        return(process_group(style_node, reference))
    elif style_node.tag == CSLNS + "names":
        return(process_names(style_node, reference))
    elif style_node.tag == CSLNS + "choose":
        return(process_choose(style_node, reference))
    elif style_node.tag == CSLNS + "text":
        return(process_text(style_node, reference))

def process_macro(macro, reference):
    """
    When given a macro and a reference, return an evaluated macro 
    (a list of FormattedNode objects).
    """
    list = [process_node(style_node, reference) for style_node in macro]
    return(list)

def process_citation(style, reference_list, citation):
    """
    With a Style, a list of References and the list of citation groups 
    (the list of citations with their locator), produce the for 
    FormattedOutput each citation group.
    """
    formatted_citation = [[process_node(style_node, citeref) for style_node in style.citation.layout] 
                             for citeref in citation]

    return(formatted_citation)

def process_bibliography(style, reference_list):
    """
    With a Style and the list of references produce a list of formatted  
    bibliographc entries.  
    """
    processed_bibliography = [[process_node(style_node, reference) for style_node in style.bibliography.layout] 
                              for reference in reference_list]

    return(processed_bibliography)

def flatten(iterable):
  it = iter(iterable)
  for e in it:
    if isinstance(e, (list, tuple)):
      for f in flatten(e):
        yield f
    else:
      yield e

def format_bibliography(processed_bibliography, format='html'):
    """
    Generates final output.
    """
    print(processed_bibliography)
    flat_bibliography = flatten(processed_bibliography)
    print(flat_bibliography)
    for formatted_reference in flat_bibliography:
        result = ""
        for formatted_node in formatted_reference:
            if format == 'html':
                result += formatted_node.to_html()
            elif format == 'text':
                result += formatted_node.to_text()
        print(result)
    
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
