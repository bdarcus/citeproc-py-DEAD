
def parse_info(csl):
    info = Info()
    return(info)


def parse_macros(csl):
    return([parse_macro(macro) for macro in macros])


def parse_macro(csl):
    macro = Macro()
    return(macro)


def parse_citation(csl):
    citation = Citation()
    return(citation)


def parse_bibliography(csl):
    bibliography = Bibliography()
    return(bibliography)


def parse_style(csl):
    info = csl.find('{http://purl.org/net/xbiblio/csl}info')
    macros = csl.findall('{http://purl.org/net/xbiblio/csl}macro')
    citation = csl.find('{http://purl.org/net/xbiblio/csl}citation') 
    bibliography = csl.find('{http://purl.org/net/xbiblio/csl}bibliography')
    info = self.parse_info(info_tree)
    macros = self.parse_macros(macros_tree)
    citation = self.parse_citation(citation_tree)
    bibliography = self.parse_bibliography(bibliography_tree)
    style = Style(info, macros, citation, bibliography)
    return(style)

