"""
Constructs a Python CSL Style class from an XML style instance.
"""
from .style import Style, Info, Option, Context, Template
from lxml import etree

NS_CSL = "{http://purl.org/net/xbiblio/csl}"

def parse_info(info_subtree):
    """
    parses the Style metadata
    """
    info_title = info_subtree.findtext(NS_CSL + 'title')
    info_id = info_subtree.findtext(NS_CSL + 'id')
    info_updated = info_subtree.findtext(NS_CSL + 'updated')
    info = Info(title=info_title, sid=info_id, updated=info_updated)
    return(info)


def parse_macros(macros_subtree):
    """
    parses the list of style macros
    """
    return([parse_macro(macro) for macro in macros_subtree])


def parse_macro(macro_subtree):
    """
    parses a macro
    """
    _name = macro_subtree.get("name")
    macro = Template(content=macro_subtree, name=_name)
    return(macro)


def parse_option(option_element):
    """
    parses a parameter option
    """
    option = Option(option_element.get("name"), option_element.get("value"))
    return(option)


def parse_options(options_list):
    """
    parses a list of parameter options
    """
    return([parse_option(option) for option in options_list])


def parse_citation(citation_subtree):
    """
    parses the citation context
    """
    options_list = citation_subtree.findall(NS_CSL + 'option')
    options = parse_options(options_list)
    citation = Context(options)
    return(citation)


def parse_bibliography(bibliography_subtree):
    """
    parses the bibliography context
    """
    options_list = bibliography_subtree.findall(NS_CSL + 'option')
    options = parse_options(options_list)
    bibliography = Context(options=options)
    return(bibliography)


def parse_style(csl_fname):
    """
    parses the CSL style
    """
    # parse the CSL file
    csl = etree.parse(csl_fname)

    # load up the main subtrees
    info_tree = csl.find(NS_CSL + 'info')
    macros_list = csl.findall(NS_CSL + 'macro')
    citation_tree = csl.find(NS_CSL + 'citation') 
    bibliography_tree = csl.find(NS_CSL + 'bibliography')

    # parse the main components, creating relavent objects
    info = parse_info(info_tree)
    macros = parse_macros(macros_list)
    citation = parse_citation(citation_tree)
    bibliography = parse_bibliography(bibliography_tree)

    # instantiate Style object
    style = Style(info, macros, citation, bibliography)
    return(style)

