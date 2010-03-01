'''
Created on 2009-10-18

@author: Marcin Biernat <biern.m@gmail.com>
'''
import wx
import os.path

from gui.plingoframe import PlingoFrame

def path_to(path):
    root_path = os.path.abspath(__file__)
    return os.path.join(root_path, path) 

def start_app():
    plingo = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    plingoFrame = PlingoFrame(None, -1, "")
    plingo.SetTopWindow(plingoFrame)
    plingoFrame.Show()
    plingo.MainLoop()


if __name__ == "__main__":
    start_app()
