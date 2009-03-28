
import json
from citeproc.csl.processor import *


def update_styles():
    """
    Updates the users' style repository.
    """
    for styles in styles:
        style.update()



def old(style_id):
    """
    Compare the last update date-time-stamp against the server 
    version. 
    """
    return(style_id['updated'] == get_style_updated(style_id))


def update(style_id):
    pass


