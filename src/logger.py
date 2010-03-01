# -*- coding: utf-8 -*-
'''
Created on 2010-03-01

@author: Marcin Biernat <biern.m@gmail.com>
'''
import logging
import logging.config

def setup_logging():
    from main import path_to
    logging.config.fileConfig(path_to("config/logging.conf"))

def log_call(log, dummy=False):
    """
    Returns decorator logging function name when it's called.
    If dummy is True then created decorator has no effect on a function.
    """
    def decorator(callable):
        def func(*args, **kwargs):
            log.debug(callable.__name__)
            return callable(*args, **kwargs)
        
        return func
    
    if not dummy:
        return decorator
    else:
        return lambda x: x
