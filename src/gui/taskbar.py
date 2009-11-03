# -*- coding: utf-8 -*-
'''
Created on 2009-10-15

@author: marcin
'''

import wx

class PlingoTaskbar(wx.TaskBarIcon):
    def __init__(self, app, *args, **kwargs):
        super(PlingoTaskbar, self).__init__(*args, **kwargs)
        self.app = app
        self.init_icon()
        self.init_menu()
        self.Bind(wx.EVT_TASKBAR_CLICK, self.OnMenu)
    
    def init_icon(self):
        bmp = wx.ArtProvider.GetBitmap("icon", wx.ART_MENU, (16,16))
        bmp.SetMask(wx.Mask(bmp, wx.WHITE))
        self.icon = wx.EmptyIcon()
        self.icon.CopyFromBitmap(bmp)
        self.SetIcon(self.icon, "Plingo")
    
    def init_menu(self):
        tm = self.menu = wx.Menu()
        #Creating menu items
        quit = wx.MenuItem(tm, wx.ID_ANY, "Exit")
        quit.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_MENU, (16,16)))
        show = wx.MenuItem(tm, wx.ID_ANY, "Show")
        show.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_MENU, (16,16)))
        #Appending them
        tm.AppendItem(show)
        tm.AppendSeparator()
        tm.AppendItem(quit)
        #Binding events
        self.Bind(wx.EVT_MENU, self.OnQuit, quit)
        self.Bind(wx.EVT_MENU, self.OnShow, show)
        
        self.Bind(wx.EVT_TASKBAR_CLICK, self.OnMenu)
        self.Bind(wx.EVT_TASKBAR_LEFT_UP, self.OnShow)

            
    def OnMenu(self, evt):
        self.PopupMenu(self.menu)
        
    def OnQuit(self, evt):
        self.app.real_exit()
        
    def OnShow(self, evt):
        self.app.show_and_rise()