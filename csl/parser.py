try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    try:
      # Python 2.5
      import xml.etree.cElementTree as etree
      print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
                print("running with cElementTree")
                except ImportError:
                    try:
                        # normal ElementTree install
                        import elementtree.ElementTree as etree
                        print("running with ElementTree")
                    except ImportError:
                        print("Failed to import ElementTree from any known place")



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
    info = self.parse_info(csl)
    macros = self.parse_macros(csl)
    citation = self.parse_citation(csl)
    bibliography = self.parse_bibliography(csl)
    style = Style(info, macros, citation, bibliography)
    return(style)

