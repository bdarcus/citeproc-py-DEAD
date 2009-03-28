
import json
from citeproc.csl.processor import *

"this needs to load a json config file"
styles_index = json.loads('x')


def update_styles():
    """
    Updates the users' style repository.
    """
    for styles in styles_index['styles']:
        style.update(style['id'])



def old(style_id):
    """
    Compare the last update date-time-stamp against the server 
    version. 
    """
    return(style_id['updated'] == get_style_updated(style_id['link']))


def update(style_id):
    pass


