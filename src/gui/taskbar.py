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
        #Loading resources
        self.hide_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_MENU, (16,16))
        self.show_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_MENU, (16,16))
        #Creating menu items
        quit = wx.MenuItem(tm, wx.ID_ANY, "Exit")
        quit.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_MENU, (16,16)))
        self.m_show = show = wx.MenuItem(tm, wx.ID_ANY, "Show")
        show.SetBitmap(self.hide_bmp)
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
        #TODO: Find a way to refresh menu items' bmp's
        if not self.app.IsIconized():
            self.menu.SetLabel(self.m_show.GetId(), "Hide")
            self.m_show.SetBitmap(self.hide_bmp)
        else:
            self.menu.SetLabel(self.m_show.GetId(), "Show")
            self.m_show.SetBitmap(self.show_bmp)
            
        self.PopupMenu(self.menu)
        
    def OnQuit(self, evt):
        self.app.real_exit()
        
    def OnShow(self, evt):
        #Or hide as well
        if self.app.IsIconized():
            self.app.show_and_rise()
        else:
            self.app.hide_to_taskbar()

