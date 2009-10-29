'''
Created on 2009-10-18

@author: marcin
'''
import wx, sys

from gui.plingoframe import PlingoFrame

def start_app():
    plingo = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    plingoFrame = PlingoFrame(None, -1, "")
    plingo.SetTopWindow(plingoFrame)
    plingoFrame.Show()
    plingo.MainLoop()


if __name__ == "__main__":
    start_app()
