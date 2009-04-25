
from .style import *
from lxml import etree

NS_CSL = "{http://purl.org/net/xbiblio/csl}"

def parse_info(info_subtree):
    info_title = info_subtree.findtext(NS_CSL + 'title')
    info_id = info_subtree.findtext(NS_CSL + 'id')
    info_updated = info_subtree.findtext(NS_CSL + 'updated')
    info = Info(title=info_title, id=info_id, updated=info_updated)
    return(info)


def parse_macros(macros_subtree):
    return([parse_macro(macro) for macro in macros_subtree])


def parse_macro(macro_subtree):
    _name = macro_subtree.get("name")
    macro = Template(content=macro_subtree, name=_name)
    return(macro)


def parse_option(option_element):
    option = Option(option_element.get("name"), option_element.get("value"))
    return(option)


def parse_options(options_list):
    return([parse_option(option) for option in options_list])


def parse_citation(citation_subtree):
    options_list = citation_subtree.findall(NS_CSL + 'option')
    options = parse_options(options_list)
    citation = Context()
    return(citation)


def parse_bibliography(bibliography_subtree):
    options_list = bibliography_subtree.findall(NS_CSL + 'option')
    options = parse_options(options_list)
    bibliography = Context(options=options)
    return(bibliography)


def parse_style(csl_fname):
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

