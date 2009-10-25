'''
Created on 2009-10-15

@author: marcin
'''

import wx, time
from wx.py.shell import ShellFrame
from wx.py.filling import FillingFrame

from generated.plingoframe import PlingoFrameGenerated
import resources

#TODO: Unicode support in textCtrls!

class PlingoFrame(PlingoFrameGenerated):
    #TODO: Make value below adjustable in properties
    auto_search_delay = 1.5
    def __init__(self, *args, **kwargs):
        super(PlingoFrame, self).__init__(*args, **kwargs)
        self.debug = kwargs.get('debug', False)
        self.init_vars()
        self.init_gui()
        self.init_input_widgets()
        self.init_frame_events()
        self.init_shortcuts()
    
    def init_vars(self):
        self.input_widget = None
        self.mode = "single"
        self.search_done = True
        self.letter_entered_timer = 0
    
    def init_frame_events(self):
        self.Bind(wx.EVT_IDLE, self.OnIdle)
    
    def init_shortcuts(self):
        #TODO: shortcuts
        pass
    
    def init_gui(self):
        self.init_gui_plugin_toolbar()
        self.init_gui_tools()
        self.init_gui_wordlist()
        if self.debug: self.init_gui_debug_panels()
        self.init_gui_search_buttons()
        self.Fit()
        self.SetMinSize(self.GetSize())
     
    def init_gui_plugin_toolbar(self):
        interfacesToolbar = wx.ToolBar(self, -1)
        interfacesToolbar.AddLabelTool(wx.ID_ANY, '', resources.load_icon('plugin'))
        interfacesToolbar.AddLabelTool(wx.ID_ANY, '', resources.load_icon('plugin'))
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
        self.wordList.InsertColumn(0, "input")
        self.wordList.InsertColumn(1, "translation")
    
    def init_gui_debug_panels(self):
        self.debugButton.Show()
        #More stuff may go here later
    
    def init_gui_search_buttons(self):
        self.searchButton = wx.BitmapButton(self, wx.ID_ANY, resources.load_icon("search"))
        self.searchButton.Bind(wx.EVT_BUTTON, self.OnSearch)
        self.translationSizer.Add(self.searchButton, 0, wx.ALL, 3)
    
    def init_gui_status_icon(self):
        #TODO: create it and hide
        pass
    
    def init_input_widgets(self):
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
        self.search_done = True
    
    def start_search(self):
        #Change status icon disable/hide buttons?
        pass
    
    def finish_search(self):
        #Change search status to finished
        pass
        
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
            self.search_done = False
            self.letter_entered_timer = time.time()
        else:
            self.search_done = True
    
    def OnDebug(self, evt):
        frame = ShellFrame(parent=self)
        frame.Show()
        frame = FillingFrame(parent=self)
        frame.Show()
        
    def OnIdle(self, evt):
        if self.search_done: return
        if time.time() - self.letter_entered_timer >= self.auto_search_delay:
            print "auto search!"
            self.search()
