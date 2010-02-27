# -*- coding: utf-8 -*-
'''
Created on 2009-10-15

@author: marcin
'''

import time
import operator
import wx, wx.animate
from wx.lib.art import flagart, img2pyartprov
from wx.py.shell import ShellFrame
from wx.py.filling import FillingFrame

from generated.plingoframe import PlingoFrameGenerated
from taskbar import PlingoTaskbar
import artprovider
import languages

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
        wx.ArtProvider.Push(artprovider.PlingoArtProvider())
        self.init_vars()
        self.init_icon()
        self.init_languages()
        self.init_gui()
        self.init_input_widgets()
        self.init_frame_events()
        self.init_shortcuts()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
    
    def init_vars(self):
        self.status_icons = {}
        self.input_widget = None
        self.mode = "single"
        self.disable_autosearch = True
        self.next_status = None
        self.letter_entered_timer = 0
    
    def init_icon(self):
        bmp = self.get_bmp("icon")
        #Transparency seems not to work with gtk
        bmp.SetMask(wx.Mask(bmp, wx.WHITE))
        self.icon = wx.EmptyIcon()
        self.icon.CopyFromBitmap(bmp)
        self.SetIcon(self.icon)
 
    def init_languages(self):
        """
        Inits all translation languages with flags available on the system 
        """
        self.languages = languages.get_languages()
    
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
        if self.debug: self.init_gui_debug_panels()
        self.init_gui_language_choices()
        self.init_gui_search_buttons()
        self.init_gui_status()
        self.init_gui_taskbar()
        self.Fit()
        self.SetMinSize(self.GetSize())
    
    def init_searchctrl(self):
        #self.searchCtrl.SetStyle bla bla bla
        pass
    
    def init_gui_plugin_toolbar(self):
        interfacesToolbar = wx.ToolBar(self, -1)
        interfacesToolbar.AddCheckLabelTool(wx.ID_ANY, '', self.get_bmp('plugin'))
        interfacesToolbar.AddCheckLabelTool(wx.ID_ANY, '', self.get_bmp('plugin'))
        interfacesToolbar.Realize()
        self.basicInterfaceSizer.Insert(0, interfacesToolbar)
        self.interfacesToolbar = interfacesToolbar   
    
    def init_gui_tools(self):
        self.preferencesButton = wx.BitmapButton(self, wx.ID_ANY, self.get_bmp("properties"))
        self.helpButton = wx.BitmapButton(self, wx.ID_ANY, self.get_bmp(wx.ART_HELP))
        self.debugButton = wx.BitmapButton(self, wx.ID_ANY, self.get_bmp('debug'))
        self.switchModeButton = wx.BitmapButton(self, wx.ID_ANY, self.get_bmp('switch_mode'))
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
            
    def init_gui_debug_panels(self):
        self.debugButton.Show()
        #More stuff may go here later
    
    def init_gui_language_choices(self):
        FlagArtProvider = img2pyartprov.Img2PyArtProvider(flagart, artIdPrefix='wx.ART_')
        wx.ArtProvider.Push(FlagArtProvider)
        self.translateFromCombo = wx.combo.BitmapComboBox(self, style=wx.CB_READONLY)
        self.translateToCombo = wx.combo.BitmapComboBox(self, style=wx.CB_READONLY)
        self.translationSizer.Insert(0, self.translateFromCombo, 1, wx.ALL, 3)
        self.translationSizer.Insert(1, self.translateToCombo, 1, wx.ALL, 3)
        #Just for testing:
        self.set_languages_to(self.languages.keys())
        self.set_languages_from(self.languages.keys())

    def init_gui_search_buttons(self):
        self.searchButton = wx.BitmapButton(self, wx.ID_ANY, self.get_bmp(wx.ART_FIND))
        self.searchButton.Bind(wx.EVT_BUTTON, self.OnSearch)
        self.translationSizer.Insert(2, self.searchButton, 0, wx.ALL, 3)
    
    def init_gui_status(self):
        font = wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL)
        self.statusText.SetFont(font)
        #static imgs
        for s in ["finished", "ready", "stopped"]:
            self.status_icons[s] = wx.StaticBitmap(self, wx.ID_ANY, 
                self.get_bmp("search_"+s))
        
        #animations
        for s in ["started"]:
            self.status_icons[s] = wx.animate.AnimationCtrl(self, wx.ID_ANY,
                self.get_animation("search_"+s))
            self.status_icons[s].Play()
            
        flags = wx.ALIGN_CENTER_VERTICAL
        for widget in self.status_icons.values():
            self.statusIconSizer.Add(widget, 0, flags)
        
        self.hide_status_icons()
        self.search_ready()
    
    def init_gui_taskbar(self):
        self.taskbar = PlingoTaskbar(self)
    
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
    
    def toggle_show_hide(self):
        if self.IsIconized():
            self.show_and_rise()
        else:
            self.hide_to_taskbar()
    
    def hide_to_taskbar(self):
        #TODO: Check if settings don't allow to iconize app
        self.Hide()
        self.Iconize(True)
        
    def show_and_rise(self):
        self.Show()
        self.Iconize(False)
        self.Raise()
        self.get_input_widget().SetFocus()
        
    def real_exit(self):
        wx.GetApp().Exit()
    
    #Shortcut functions for wx.ArtProvider
    def get_bmp(self, art_name_or_id):
        return wx.ArtProvider.GetBitmap(art_name_or_id, wx.ART_MENU, (16,16))
    
    def get_animation(self, name):
        #Relays on ArtProvider implementing this method!
        return artprovider.get_animation(name)
    
    def set_languages_from(self, codes_list):
        """ 
        Codes list element may be a string matching existing language code
        or tuple defining new language: (code, <name, <flag_bmp>>).
        if flag_bmp is not present, app will try to determine flag from
        language code. Same with 'name'.
        """
        for line in self.parse_codes_list(codes_list):
            self.translateFromCombo.Append(*line)
    
    def set_languages_to(self, codes_list):
        """
        See "set_languages_from"
        """ 
        for line in self.parse_codes_list(codes_list):
            self.translateToCombo.Append(*line)
    
    def parse_codes_list(self, codes_list):
        """
        Returns sorted list of (name, bmp, country_code) that is ready to fill
        BitmapComboBox. Codes list is the same format as in set_languages_from
        """
        result = []
        lang = []
        for value in codes_list:
            #If value is language code then
            if type(value) in (unicode, str):
                #If value is shorter code form, get full one
                parsed_code = languages.parse_country_code(value)
                try:
                    lang = self.languages[parsed_code]
                except KeyError:
                    print('Unknown language code "{0}", ({1} originally)'.format(parsed_code, value))
                    lang = value
                
                result.append([lang, languages.flag_for(parsed_code), value])
                
            else:
                code = value[0]
                parsed_code = languages.parse_country_code(code)
                name = None
                #Get name from tuple if possible, else get it from code
                if len(value) > 1:
                    name = value[1]
                else:
                    try:
                        name = self.languages[parsed_code]
                    except KeyError:
                        name = code
                
                bmp = languages.flag_for(parsed_code)
                if len(value) > 2:
                    bmp = wx.Bitmap(value[2])
                
                result.append([name, bmp, code])
        
        return sorted(result, key=operator.itemgetter(2)) 

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
    
    def get_input_widget(self):
        if self.mode == 'single':
            return self.searchCtrl
        else:
            return self.searchCtrlMulti
    
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

    def OnClose(self, evt):
        #TODO: Check if settings don't allow to iconize app
        self.hide_to_taskbar()

