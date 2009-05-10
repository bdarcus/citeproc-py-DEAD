import os
import glob
from parser import parse_style
from operator import itemgetter

def load_styles():
    styles = []
    for style in glob.glob(os.path.expanduser("~/Code/zotero-csl/*.csl")):
        print "loading ", style
        parse_style(style)
        styles.append(parse_style(style))
    return(styles)

styles = load_styles()

def analyze_macros(styles):
    pass

def macro_names(styles):
    names = {}
    print("Macro Names and Counts")
    print("======================")
    for style in styles:
        for macro in style.macros:
            name = macro.name 
            if names.has_key(name):
                names[name] += 1
            else:
                names[name] = 1

    for k, v in sorted(names.items(), reverse=True, key=itemgetter(1)):
        print "   ", k, ": ", v 


macro_names(styles)
