# -*- coding: utf-8 -*-
'''
Created on 2009-10-26

@author: marcin
'''

import wx, wx.animate, os

#global so that other functions can use that
#(it is impossible to add use extra methods of wx.ArtProvider descendant)
custom_resources = {}

def get_animation(name):
    return custom_resources[name]

class PlingoArtProvider(wx.ArtProvider):
    custom_resources = custom_resources
    img_to_load = {
        "properties" : "cog.png",
        "debug" : "bricks.png",
        "switch_mode" : "text_linespacing.png",
        "plugin": "plugin.png",
    }
    anim_to_load = {
        "search_started": "anim/ajax-loader.gif",
    }
    aliases = {
        "search_finished": wx.ART_INFORMATION,
        "search_stopped" : wx.ART_DELETE,
        "search_ready": wx.ART_TICK_MARK,
    }
    def __init__(self):
        #Only old style parent init seems to work
        wx.ArtProvider.__init__(self)
        self.load_custom_resources()
    
    def resource_path(self, path):
        return os.path.join(os.path.dirname(__file__), "../icons/", path)
    
    def load_custom_resources(self):
        for name, path in self.img_to_load.items():
            self.custom_resources[name] = wx.Bitmap(self.resource_path(path))
            
        for name, path in self.anim_to_load.items():
            self.custom_resources[name] = wx.animate.Animation(self.resource_path(path))
        
    def CreateBitmap(self, artid, client, size):
        
        bmp = wx.NullBitmap
        if size.width != 16:
            #None other custom icon sizes available
            return bmp
        
        try:
            return self.GetBitmap(self.aliases[artid], client, size)
        except KeyError:
            pass
        
        try:
            return self.custom_resources[artid]
        except KeyError:
            return bmp
        
        return bmp
