'''
Created on 2009-10-29

@author: marcin
'''
#list format: (cc, name, bmp, wx.ID)

import os
import wx
from wx.lib import langlistctrl
from wx.tools import img2py

import data

FILENAME = "languages.pickle"
INFO_FILENAME = "languages_info.txt"

def flag_for(country_code):
    cnt = country_code.split('_')[1].upper()
    return wx.ArtProvider.GetBitmap('wx.ART_'+cnt, wx.ART_OTHER, (16,11))

def build_languages():
    result = {}
    lrl = langlistctrl.CreateLanguagesResourceLists(filter=langlistctrl.LC_ALL)
    country_mappings = langlistctrl.BuildLanguageCountryMapping()
    for name, lid in zip(*lrl[1:]):
        #Can't save wx bmps in pickle
        result[country_mappings[lid]] = name
    
    return result

def get_languages():
    return data.LANGUAGE_CODES

def generate_languages_info_file(data):
    file = open(INFO_FILENAME, 'w')
    lines = []
    for k in sorted(data.keys()):
        lines.append("{0:6} : {1},\n".format('"'+k+'"', '"'+data[k]+'"'))
        
    file.writelines(lines)
    file.close()

def parse_country_code(code):
    code = code.strip()
    try:
        code = data.LANGUAGE_CODES_MAPPINGS[code]
    except KeyError:
        pass
        
    if '_' not in code:
        code += '_'+code.upper()
        
    return code