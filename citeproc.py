"""
For processing citations and bibliographies using the Citation Style 
Language (CSL).

>>> STYLE = Style('apa.csl')
>>> REFS = json.loads(open('refs.json').read())
>>> PROCESSED = process_bibliography(STYLE, REFS)
>>> format_bibliography(PROCESSED)
"""
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
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
            self.citation.layout = self.citation.find(CSLNS + 'layout')
            self.citation.options = self.citation.findall(CSLNS + 'option')

        if self.bibliography:
            self.bibliography.options = self.bibliography.find(CSLNS + 'option')
            self.bibliography.layout = self.bibliography.find(CSLNS + 'layout')



# >>> processing functions <<<

def get_macro(name, macros):
    """
    Return macro from macro list by name.
    """
    for themacro in (macro for macro in macros if macro.get('name') == name):
        if themacro:
            return(themacro)
        else:
            pass

def get_property(lname):
    """
    When given a CSL variable name, returns the corresponding RDF property.
    """
    pmap = { 
        "title": "dcterms:title", 
        "issued": "dcterms:issued",
        "volume": "bibo:volume",
        "issue": "bibo:issue",
        "doi": "bibo:doi",
        "uri": "bibo:uri",
        "isbn": "bibo:isbn",
        # return a dict for relations; need to adjust other code
        "container-title": {"dcterms:isPartOf": "dcterms:title"}
        }
    return(pmap[lname])

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

def format_name(name_node, contributor):
    pass

def substitute(substitute_node, reference):
    pass

def process_names(names_node, reference):
    """
    When given a style node and a reference, returns an evaluated list of 
    contributor names.
    """
    roles = names_node.get('variable').split(' ')
    substitute_node = names_node.find(CSLNS + 'substitute')

    for role in roles:
        if role in reference:
            for contributor in reference[role]:
                format_name(names_node.find(CSLNS + name), contributor)
        else:
            substitute(substitute_node, reference)

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

def process_children(parent, style_node, style_macros, reference):
    children = style_node.getchildren()
    for child in children:
        return(process_node(parent, child, style_macros, reference))

def process_choose(parent, style_node, style_macros, reference):
    """
    When given a style node and a reference, return an evaluated cs:choose.
    """
    children = style_node.getchildren()

    for child in children:
        # first we check if there are attributes; if there are, it means
        # the node is either a cs:if or a cs:else-if element
        if child.attrib:
            if condition(child.attrib, reference):
                return(process_children(parent, child, style_macros, reference))
        else:
            process_children(parent, child, style_macros, reference)

def process_text(parent, style_node, style_macros, reference):
    """
    When given a style node and a reference, return an evaludated cs:text.
    """
    formatting = style_node.attrib
    variable = style_node.get('variable')
    macro = style_node.get('macro')
    
    if variable:
        content = reference[style_node.get('variable')] if variable in reference else None
        if content:
            node = SubElement(parent, "span", attrib=formatting)
            node.set('property', get_property(node.attrib.pop('variable')))
            node.text = content
            return(node)
    elif macro:
        macro_result = process_macro(parent, get_macro(macro, style_macros), style_macros, reference)
        return(macro_result)
    else:
        pass

def process_node(parent, style_node, style_macros, reference):
    """
    Passes of style node processing to appropriate function.
    """
    if style_node.tag == CSLNS + "group":
        return(process_group(style_node, reference))
    elif style_node.tag == CSLNS + "names":
        return(process_names(style_node, reference))
    elif style_node.tag == CSLNS + "choose":
        return(process_choose(parent, style_node, style_macros, reference))
    elif style_node.tag == CSLNS + "text":
        return(process_text(parent, style_node, style_macros, reference))

def process_macro(parent, macro, style_macros, reference):
    """
    When given a macro and a reference, return an evaluated macro 
    (a list of FormattedNode objects).
    """
    mlist = [process_node(parent, style_node, style_macros, reference) for style_node in macro]
    return(mlist)

def process_citation(style, reference_list, citation):
    """
    With a Style, a list of References and the list of citation groups 
    (the list of citations with their locator), produce the
    formatted output for each citation group.
    """
    processed_citation = Element("span", attrib={"class":"citation"})

    for reference in reference_list:
        citeref = SubElement(processed_citation, "span")
        for style_node in style.citation.layout:
            process_node(citeref, style_node, style.macros, reference) 

    return(processed_citation)

def process_bibliography(style, reference_list):
    """
    With a Style and the list of references produce a list of formatted  
    bibliographc entries.  
    """
    processed_bibliography = Element("ol", attrib={"class":"bibliography"})

    for reference in reference_list:
        ref = SubElement(processed_bibliography, "li", attrib={"property":"dcterms:references"})
        for style_node in style.bibliography.layout:
            process_node(ref, style_node, style.macros, reference) 

    return(processed_bibliography)

def format_bibliography(processed_bibliography, oformat='html+rdfa'):
    """
    Generates final output.
    """
    if oformat == 'html+rdfa':
        print(tostring(processed_bibliography))
    elif oformat == 'text':
        result = ""
        for node in processed_bibliography.getiterator():
            if node.text:
                result += node.text
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
