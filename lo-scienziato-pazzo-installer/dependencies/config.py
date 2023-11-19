# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Parámetros de configuración (kodi)
# ------------------------------------------------------------

#from builtins import str
import sys
PY3 = False
if sys.version_info[0] >= 3: PY3 = True; unicode = str; unichr = chr; long = int

import os
import re

import xbmc
import xbmcaddon

PLUGIN_NAME = "lo-scienziato-pazzo"

__settings__ = xbmcaddon.Addon(id="plugin.video." + PLUGIN_NAME)
__language__ = __settings__.getLocalizedString


def get_platform(full_version=False):
    """
        Returns the information about the version of xbmc or kodi on which the plugin is executed

        @param full_version: indicates whether we want all the information or not
        @type full_version: bool
        @rtype: str or dict
        @return: If the full_version parameter is True, a dictionary with the following keys is returned:
            'num_version': (float) version number in XX.X format
            'name_version': (str) key name of each version
            'platform': (str) is composed of "kodi-" or "xbmc-" plus the version name as appropriate.
        If the full_version parameter is False (default), the value of the 'platform' key from the previous dictionary is returned.
    """
        
    ret = {}
    codename = {"10": "dharma", "11": "eden", "12": "frodo",
                "13": "gotham", "14": "helix", "15": "isengard",
                "16": "jarvis", "17": "krypton", "18": "leia", 
                "19": "matrix"}
    code_db = {'10': 'MyVideos37.db', '11': 'MyVideos60.db', '12': 'MyVideos75.db',
               '13': 'MyVideos78.db', '14': 'MyVideos90.db', '15': 'MyVideos93.db',
               '16': 'MyVideos99.db', '17': 'MyVideos107.db', '18': 'MyVideos116.db', 
               '19': 'MyVideos119.db'}

    num_version = xbmc.getInfoLabel('System.BuildVersion')
    num_version = re.match("\d+\.\d+", num_version).group(0)
    ret['name_version'] = codename.get(num_version.split('.')[0], num_version)
    ret['num_version'] = float(num_version)
    if ret['num_version'] < 14:
        ret['platform'] = "xbmc-" + ret['name_version']
    else:
        ret['platform'] = "kodi-" + ret['name_version']

    if full_version:
        return ret
    else:
        return ret['platform']


def get_localized_string(code):
    dev = __language__(code)

    try:
        # Unicode to utf8
        if isinstance(dev, unicode):
            dev = dev.encode("utf8")
            if PY3: dev = dev.decode("utf8")

        # All encodings to utf8
        elif not PY3 and isinstance(dev, str):
            dev = unicode(dev, "utf8", errors="replace").encode("utf8")
        
        # Bytes encodings to utf8
        elif PY3 and isinstance(dev, bytes):
            dev = dev.decode("utf8")
    except:
        pass

    return dev


def get_icon():
    return xbmc.translatePath(__settings__.getAddonInfo('icon'))


def get_fanart():
    return xbmc.translatePath(__settings__.getAddonInfo('fanart'))
