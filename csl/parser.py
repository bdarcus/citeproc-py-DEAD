
from style import *

def parse_info(info_subtree):
    info_title = info_subtree.findtext('{http://purl.org/net/xbiblio/csl}title')
    info_id = info_subtree.findtext('{http://purl.org/net/xbiblio/csl}id')
    info_updated = info_subtree.findtext('{http://purl.org/net/xbiblio/csl}updated')
    info = Info(title=info_title, id=info_id, updated=info_updated)
    return(info)


def parse_macros(macros_subtree):
    return([parse_macro(macro) for macro in macros_subtree])


def parse_macro(macro_subtree):
    macro = Macro()
    return(macro)


def parse_option(option_element):
    option = Option()
    return(option)


def parse_options(options_list):
    return([parse_option(option) for option in options_list])


def parse_citation(citation_subtree):
    options_list = citation_subtree.findall('{http://purl.org/net/xbiblio/csl}option')
    options = parse_options(options_list)
    citation = Citation()
    return(citation)


def parse_bibliography(bibliography_subtree):
    options_list = bibliography_subtree.findall('{http://purl.org/net/xbiblio/csl}option')
    options = parse_options(options_list)
    bibliography = Bibliography()
    return(bibliography)


def parse_style(csl_fname):
    csl = etree.parse(csl_fname)
    info_tree = csl.find('{http://purl.org/net/xbiblio/csl}info')
    macros_list = csl.findall('{http://purl.org/net/xbiblio/csl}macro')
    citation_tree = csl.find('{http://purl.org/net/xbiblio/csl}citation') 
    bibliography_tree = csl.find('{http://purl.org/net/xbiblio/csl}bibliography')
    info = parse_info(info_tree)
    macros = parse_macros(macros_list)
    citation = parse_citation(citation_tree)
    bibliography = parse_bibliography(bibliography_tree)
    style = Style(info, macros, citation, bibliography)
    return(style)

