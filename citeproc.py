"""
For processing citations and bibliographies using the Citation Style 
Language (CSL).

>>> STYLE = Style('apa.csl')
>>> REFS = json.loads(open('refs.json').read())
>>> PROCESSED = process_bibliography(STYLE, REFS)
>>> format_bibliography(PROCESSED)
"""
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring

try:
    import simplejson as json
except:
    import json

CSLNS = '{http://purl.org/net/xbiblio/csl}'

# >>> classes <<<

class Style():
    """
    An ElementTree wrapper to easily parse and work with a CSL instance.
    >>> style = Style('some.csl')
    >>> style.title
    "Some Style"
    """

    def __init__(self, csl_fname):
        _style = ElementTree()
        _style.parse(csl_fname)
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
        "author": "dc:creator",
        "editor": "bibo:editor",
        "translator": "bibo:translator",
        "title": "dc:title", 
        "issued": "dc:issued",
        "volume": "bibo:volume",
        "issue": "bibo:issue",
        "doi": "bibo:doi",
        "uri": "bibo:uri",
        "isbn": "bibo:isbn",
        # return a dict for relations; need to adjust other code
        "container-title": {"dc:isPartOf": "dc:title"},
        "publisher": {"dc:publisher": "foaf:name"}
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

def initialize(name, init_with):
    return(init_with.join(part[0] for part in name.split(" ")) + init_with)

def format_name(parent, name_node, contributor, role, swap=False):
    contributor_node = SubElement(parent, "span")
    contributor_node.set('property', get_property(role))

    if contributor['given'] and contributor['family']:

        contributor_node.set('typeOf', 'foaf:Person')

        init_with = name_node.get('initialize-with')
        display_as_sort = contributor.get('display-as-sort')

        if display_as_sort or swap:
            fname = SubElement(contributor_node, 'span')
            fname.set('property', 'foaf:surname')
            fname.text = contributor['family']
            fname.tail = ", " if swap else " "
        
            gname = SubElement(contributor_node, 'span')
            gname.set('property', 'foaf:givenname')

            if init_with:
                if display_as_sort:
                    gname.text = contributor['given']
                else:
                    gname.set('content', contributor['given'])
                    gname.text = initialize(contributor['given'], init_with)
        else:
            gname = SubElement(contributor_node, 'span')
            gname.set('property', 'foaf:givenname')
            if init_with:
                gname.set('content', contributor['given'])
                gname.text = initialize(contributor['given'], init_with)
            else:
                gname.set('content', contributor['given'])
            gname.tail = " "

            fname = SubElement(contributor_node, 'span')
            fname.set('property', 'foaf:surname')
            fname.text = contributor['family']

    elif contributor['name']:
        # we assume we have an organization
        contributor_node.set('typeOf', 'foaf:Organization')
        name = SubElement(contributor_node, 'span')
        name.set('property', 'foaf:name')
        name.text = contributor['name']
    
    return(contributor_node)

def substitute(parent, substitute_node, style_macros, reference):
    children = substitute_node.getchildren()

    for child in children:
        processed_node = process_node(parent, child, style_macros, reference)
        if processed_node:
            return(processed_node)
        else:
            pass

def process_names(parent, names_node, style_macros, reference, display=True):
    """
    When given a style node and a reference, returns an evaluated list of 
    contributor names.
    """
    roles = names_node.get('variable').split(' ')
    substitute_node = names_node.find(CSLNS + 'substitute')

    for role in roles:
        if role in reference:
            if display:
                # grab the list of formatted names, according to the 
                # CSL definitions
                for contributor in reference.pop(role):
                    format_name(parent, 
                                names_node.find(CSLNS + 'name'), 
                                contributor, role)
            else:
                # return a string representation of the names for sorting
                (":").join(reference[role])    
        else:
            substitute(parent, substitute_node, style_macros, reference)

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
        if variable in reference:
            content = reference.pop(style_node.get('variable'))
        else:
            content = None

        if content:
            node = SubElement(parent, "span", attrib=formatting)
            node.set('property', get_property(node.attrib.pop('variable')))
            node.text = content
            return(node)
    elif macro:
        macro_result = process_macro(parent, 
                                     get_macro(macro, style_macros), 
                                     style_macros, 
                                     reference)
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
        return(process_names(parent, style_node, style_macros, reference))
    elif style_node.tag == CSLNS + "choose":
        return(process_choose(parent, style_node, style_macros, reference))
    elif style_node.tag == CSLNS + "text":
        return(process_text(parent, style_node, style_macros, reference))

def process_macro(parent, macro, style_macros, reference):
    """
    When given a macro and a reference, return an evaluated macro 
    (a list of FormattedNode objects).
    """
    mlist = [process_node(parent, style_node, style_macros, reference) 
             for style_node in macro]
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
        ref = SubElement(processed_bibliography, "li", 
                         attrib={"property":"dc:references"})

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
