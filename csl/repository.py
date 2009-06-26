import os
import glob
from parser import parse_style, NS_CSL
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


def macro_calls(styles):
    calls = {}
    print "Analyzing macro calls ..."
    for style in styles:
        if style.bibliography:
            for text in style.bibliography.layout.findall(NS_CSL + 'text'):
                print "Macro Calls and Counts for Bibliography"
                print "======================"
                if calls.has_key(text.get('macro')):
                    calls[text.get('macro')] += 1
                else:
                    calls[text.get('macro')] = 1
        
    else:
            print "    no macro calls"

    for k, v in sorted(calls.items(), reverse=True, key=itemgetter(1)):
        print "   ", k, ": ", v


macro_names(styles)
macro_calls(styles)
