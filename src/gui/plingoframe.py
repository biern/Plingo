# -*- coding: utf-8 -*-
'''
Created on 2009-10-15

@author: marcin
'''

import wx, time, wx.animate
from wx.py.shell import ShellFrame
from wx.py.filling import FillingFrame

from generated.plingoframe import PlingoFrameGenerated
import resources

#TODO: Unicode support in textCtrls!

sample_wordlist = {
                   "python": ['pyton', 'wąż'],
                   "blablabla":['niewiadomoco']}



class PlingoFrame(PlingoFrameGenerated):
    messages  = {
                         "search_started": "searching...",
                         "search_stopped": "stopped",
                         "search_finished": "finished",
                         "search_ready":"ready",
                         }
    #TODO: Make value below adjustable in properties
    auto_search_delay = 1.5
    def __init__(self, *args, **kwargs):
        super(PlingoFrame, self).__init__(*args, **kwargs)
        self.debug = kwargs.get('debug', True)
        self.init_vars()
        self.init_gui()
        self.init_input_widgets()
        self.init_frame_events()
        self.init_shortcuts()
    
    def init_vars(self):
        self.status_icons = {}
        self.input_widget = None
        self.mode = "single"
        self.disable_autosearch = True
        self.next_status = None
        self.letter_entered_timer = 0
    
    def init_frame_events(self):
        self.Bind(wx.EVT_IDLE, self.OnIdle)
    
    def init_shortcuts(self):
        #TODO: shortcuts
        pass
    
    def init_gui(self):
        self.init_searchctrl()
        self.init_gui_plugin_toolbar()
        self.init_gui_tools()
        self.init_gui_wordlist()
        self.init_gui_languages()
        if self.debug: self.init_gui_debug_panels()
        self.init_gui_search_buttons()
        self.init_gui_status()
        self.Fit()
        self.SetMinSize(self.GetSize())
    
    def init_searchctrl(self):
        #self.searchCtrl.SetStyle bla bla bla
        pass
    
    def init_gui_plugin_toolbar(self):
        interfacesToolbar = wx.ToolBar(self, -1)
        interfacesToolbar.AddCheckLabelTool(wx.ID_ANY, '', resources.load_icon('plugin'))
        interfacesToolbar.AddCheckLabelTool(wx.ID_ANY, '', resources.load_icon('plugin'))
        interfacesToolbar.Realize()
        self.basicInterfaceSizer.Insert(0, interfacesToolbar)
        self.interfacesToolbar = interfacesToolbar   
    
    def init_gui_tools(self):
        self.preferencesButton = wx.BitmapButton(self, wx.ID_ANY, resources.load_icon('properties'))
        self.helpButton = wx.BitmapButton(self, wx.ID_ANY, resources.load_icon('help'))
        self.debugButton = wx.BitmapButton(self, wx.ID_ANY, resources.load_icon('debug'))
        self.switchModeButton = wx.BitmapButton(self, wx.ID_ANY, resources.load_icon('switch_mode'))
        #Binding events
        self.debugButton.Bind(wx.EVT_BUTTON, self.OnDebug)
        self.switchModeButton.Bind(wx.EVT_BUTTON, self.OnSwitchMode)
        #Adding buttons to sizer
        self.menuSizer.Insert(0, self.preferencesButton, 0, wx.ALL, 3)
        self.menuSizer.Insert(1, self.helpButton, 0, wx.ALL, 3)
        self.menuSizer.Insert(2, self.switchModeButton, 0, wx.ALL, 3)
        self.menuSizer.Insert(3, self.debugButton, 0, wx.ALL, 3)
        
        self.debugButton.Hide()
    
    def init_gui_wordlist(self):
        #TODO: Hide it before search?
        self.wordList.populate(sample_wordlist)
        
    
    def init_gui_languages(self):
        #TODO: Load resources for BitmapComboBox
        pass
    
    def init_gui_debug_panels(self):
        self.debugButton.Show()
        #More stuff may go here later
    
    def init_gui_search_buttons(self):
        self.searchButton = wx.BitmapButton(self, wx.ID_ANY, resources.load_icon("search"))
        self.searchButton.Bind(wx.EVT_BUTTON, self.OnSearch)
        self.translationSizer.Add(self.searchButton, 0, wx.ALL, 3)
    
    def init_gui_status(self):
        font = wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL)
        self.statusText.SetFont(font)
        #static imgs
        for s in ["finished", "ready", "stopped"]:
            self.status_icons[s] = wx.StaticBitmap(self, wx.ID_ANY, 
                resources.load_icon("search_"+s))
        
        #animations
        for s in ["started"]:
            self.status_icons[s] = wx.animate.AnimationCtrl(self, wx.ID_ANY,
                resources.load_icon("search_"+s, wx.animate.Animation))
            self.status_icons[s].Play()
            
        flags = wx.ALIGN_CENTER_VERTICAL
        for widget in self.status_icons.values():
            self.statusIconSizer.Add(widget, 0, flags)
        
        self.hide_status_icons()
        self.search_ready()
    
    def init_input_widgets(self):
        #TODO: use searchCtrl!
        self.hide_input_widgets()
        self.init_singleline_mode()
    
    def init_multiline_mode(self):
        self.hide_input_widgets()
        self.searchCtrlMulti.Show()
        self.searchCtrlMulti.Value = self.get_input_text()
        self.Layout()
        self.mode = "multi"
        self.search()
    
    def init_singleline_mode(self):
        self.hide_input_widgets()
        self.searchCtrl.Show()
        self.searchCtrl.Value = self.get_input_text()
        self.Layout()
        self.mode = "single"
        self.search()
    
    #================================================================================
    # Helper functions
    #================================================================================
    
    def set_next_status_timed(self, delay, status, msg=None):
        self.next_status = {}
        self.next_status['status'] = status
        self.next_status['msg'] = msg
        self.next_status['time'] = time.time() + delay
    
    def hide_status_icons(self, hide=True):
        self.statusIconSizer.ShowItems(not hide)
        
    def hide_input_widgets(self):
        self.searchCtrl.Hide()
        self.searchCtrlMulti.Hide()
    
    def switch_modes(self):
        if self.mode == "single":
            self.init_multiline_mode()
        else:
            self.init_singleline_mode()
    
    def get_input_text(self):
        if self.mode == "single":
            return self.searchCtrl.Value
        else:
            return self.searchCtrlMulti.Value
    
    def search(self):
        if not self.get_input_text(): return
        print("Searching for \"{0}\"".format(self.get_input_text()))
        #search done shoud be returned by plugin?
        self.disable_autosearch = True
        self.search_started()
    
    def stop_search(self):
        pass
    
    def set_status(self, msg=None, search_status=None):
        """
        At least 1 arg is required. This function calls 'search_*' functions if available
        """
        setter = getattr(self, 'search_' + search_status, None)
        if setter:
            setter(msg)
        else:
            self.__set_status(msg, search_status)

    def search_started(self, msg=None):
        """ 
        Works like set_status' callback but can be called instead of it, 
        should always call __set_status
        """            
        self.__set_status(msg, "started")
        self.set_next_status_timed(3, 'finished')
    
    def search_finished(self, msg=None):
        self.__set_status(msg, "finished")
        self.set_next_status_timed(3, 'ready')
    
    def search_stopped(self, msg=None):
        self.__set_status(msg, "stopped")
    
    def search_ready(self, msg=None):
        self.__set_status(msg, "ready")
    
    def __set_status(self, msg=None, search_status=None):
        """
        Requires at least 1 arg (will set blank status otherwise)
        Use search_* methods instead of this one in plugins!
        """
        self.next_status = None
        self.hide_status_icons()
        try:
            self.status_icons[search_status].Show()
        except KeyError:
            pass
                
        default_msg = ""
        if search_status:
            default_msg = self.messages.get("search_"+search_status, "")
            
        if not msg: 
            msg = default_msg
        elif msg.startswith("+"): 
            msg = default_msg + msg
            
        self.statusText.SetLabel(msg)
        self.Layout()

        
    #================================================================================
    # Event handlers   
    #================================================================================
    def OnSearch(self, evt):
        self.search()
        
    def OnSwitchMode(self, evt):
        self.switch_modes()
    
    def OnTextSubmited(self, evt):
        self.search()
    
    def OnLetterEntered(self, evt):
        if len(self.get_input_text()):
            self.disable_autosearch = False
            self.letter_entered_timer = time.time()
        else:
            self.disable_autosearch = True
    
    def OnDebug(self, evt):
        frame = ShellFrame(parent=self)
        frame.Show()
        frame = FillingFrame(parent=self)
        frame.Show()
        
    def OnIdle(self, evt):
        if not self.disable_autosearch:
            if time.time() - self.letter_entered_timer >= self.auto_search_delay:
                print "auto search!"
                self.search()
        
        if self.next_status:
            if time.time() - self.next_status['time'] >= 0:
                self.set_status(self.next_status['msg'], self.next_status['status'])
