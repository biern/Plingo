# -*- coding: utf-8 -*-
'''
Created on 2009-10-26

@author: marcin
'''

import wx, sys
import  wx.lib.mixins.listctrl  as  listmix


class WordList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        #TODO: Make this show items multiline somehow
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        self.InsertColumn(0, "input")
        self.InsertColumn(1, "translation")
        listmix.ListCtrlAutoWidthMixin.__init__(self)
    
    def clear(self):
        #alias
        self.DeleteAllItems()
        
    def populate(self, items, append=False):
        """
        Items is a dict of words, each with a list of possible meanings 
        """
        #TODO: Fix columns width to ensure that first column is visible
        if not append:
            self.clear()
            
        for key, meanings in items.items():
            index = self.InsertStringItem(sys.maxint, key)
            for i, word in enumerate(meanings):
                if i:
                    self.InsertStringItem(sys.maxint, "")
                self.SetStringItem(index, 1, word)
                index += 1
        
        
