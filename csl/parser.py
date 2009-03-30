
def parse_info(info_subtree):
    info = Info()
    return(info)


def parse_macros(macros_subtree):
    return([parse_macro(macro) for macro in macros_subtree])


def parse_macro(macro_subtree):
    macro = Macro()
    return(macro)


def parse_citation(citation_subtree):
    citation = Citation()
    return(citation)


def parse_bibliography(bibliography_subtree):
    bibliography = Bibliography()
    return(bibliography)


def parse_style(csl_fname):
    csl = etree.parse(csl_fname)
    info_tree = csl.find('{http://purl.org/net/xbiblio/csl}info')
    macros_tree = csl.findall('{http://purl.org/net/xbiblio/csl}macro')
    citation_tree = csl.find('{http://purl.org/net/xbiblio/csl}citation') 
    bibliography_tree = csl.find('{http://purl.org/net/xbiblio/csl}bibliography')
    info = parse_info(info_tree)
    macros = parse_macros(macros_tree)
    citation = parse_citation(citation_tree)
    bibliography = parse_bibliography(bibliography_tree)
    style = Style(info, macros, citation, bibliography)
    return(style)

