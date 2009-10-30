'''
Created on 2009-10-29

@author: marcin
'''
#list format: (cc, name, bmp, wx.ID)

import pickle
import os
import wx
from wx.lib import langlistctrl
from wx.tools import img2py

FILENAME = "languages.pickle"
INFO_FILENAME = "languages_info.txt"

def flag_for(country_code):
    cnt = country_code.split('_')[1].upper()
    return wx.ArtProvider.GetBitmap('wx.ART_'+cnt, wx.ART_OTHER, (16,11))

def load_languages():
    if os.path.exists(FILENAME):
        file = open(FILENAME)
        return pickle.load(file)
    else:
        return build_languages()

def build_languages():
    result = {}
    lrl = langlistctrl.CreateLanguagesResourceLists(filter=langlistctrl.LC_ALL)
    country_mappings = langlistctrl.BuildLanguageCountryMapping()
    for name, lid in zip(*lrl[1:]):
        #Can't save wx bmps in pickle
        result[country_mappings[lid]] = name
    
    file = open(FILENAME, 'w')
    pickle.dump(result, file)
    generate_languages_info_file(result)
    return result


def generate_languages_info_file(data):
    file = open(INFO_FILENAME, 'w')
    lines = []
    for k in sorted(data.keys()):
        lines.append("{0:6} : {1}\n".format(k, data[k]))
        
    file.writelines(lines)
    file.close()
