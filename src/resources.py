'''
Created on 2009-10-18

@author: marcin
'''
import wx, os

ICONS_PATH = os.path.join(os.path.dirname(__file__), "../icons/")
LOADED_RESOURCES = {}
#TODO: Switch to wx.ArtProvider for native icons

# mappings to make life easier
# note that you don't have to use that mappings
ICON_NAMES_MAPPING = {
    "properties" : "cog.png",
    "help" : "help.png",
    "debug" : "bricks.png",
    "switch_mode" : "text_linespacing.png",
    "plugin": "plugin.png",
    "search": "find.png",
    "search_started": "anim/ajax-loader.gif",
    "search_stopped": "plugin.png",
    "search_ready":"plugin.png",
    "search_finished":"plugin.png",
    }

def init_resources():
    LOADED_RESOURCES['icons'] = {}

def load_icon(icon_name, method=wx.Bitmap):
    """
    Loads icon on demand (lazy), makes use of ICON_NAMES_MAPPING defined above
    """
    icon_name = icon_name.strip()
    #Check if icon_name is mapped to a path. If not treat it as a normal path
    try:
        icon_name = ICON_NAMES_MAPPING[icon_name]
    except KeyError:
        pass
    
    #Return resource if it was already loaded, else load and save it for later.
    try:
        return LOADED_RESOURCES['icons'][icon_name]
    except KeyError:
        loaded = method(os.path.join(ICONS_PATH, icon_name))
        LOADED_RESOURCES['icons'][icon_name]= loaded
        return loaded
