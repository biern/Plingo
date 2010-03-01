'''
Created on 2009-10-18

@author: Marcin Biernat <biern.m@gmail.com>
'''
import wx
import os.path

from gui.plingoframe import PlingoFrame
import logger

def path_to(path):
    """
    Returns path to root app data directory
    """
    root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '../')
    return os.path.join(root_path, path) 

def start_app():
    plingo = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    plingoFrame = PlingoFrame(None, -1, "")
    plingo.SetTopWindow(plingoFrame)
    plingoFrame.Show()
    plingo.MainLoop()


if __name__ == "__main__":
    logger.setup_logging()
    start_app()
