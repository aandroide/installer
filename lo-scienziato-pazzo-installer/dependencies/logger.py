# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------
# Logger (kodi)
# --------------------------------------------------------------------------------
from __future__ import unicode_literals
import inspect, os, xbmc, sys

LOG_FORMAT = '{addname}[{filename}.{function}:{line}]{sep} {message}'
DEBUG_ENABLED = True
DEF_LEVEL = xbmc.LOGINFO if sys.version_info[0] >= 3 else xbmc.LOGNOTICE


def info(*args):
    log(*args)


def debug(*args):
    if DEBUG_ENABLED:
        log(*args)


def error(*args):
    log("######## ERROR #########", level=xbmc.LOGERROR)
    log(*args, level=xbmc.LOGERROR)


def log(*args, **kwargs):
    msg = ''
    for arg in args: msg += ' ' + str(arg)
    frame = inspect.currentframe().f_back.f_back
    filename = frame.f_code.co_filename
    filename = os.path.basename(filename).split('.')[0]
    xbmc.log(LOG_FORMAT.format(addname="lo-scienziato-pazzo-installer",
                              filename=filename,
                              line=frame.f_lineno,
                              sep=':' if msg else '',
                              function=frame.f_code.co_name,
                              message=msg), kwargs.get('level', DEF_LEVEL))


class WebErrorException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
