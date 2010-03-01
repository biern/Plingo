# -*- coding: utf-8 -*-
'''
Created on 2010-03-01

@author: Marcin Biernat <biern.m@gmail.com>
'''
import logging
import logging.config

from main import path_to

def setup_logging():
    logging.config.fileConfig(path_to("config/logging.conf"))

