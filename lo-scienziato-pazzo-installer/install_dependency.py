# -*- coding: utf-8 -*-
import io
import platform
import xbmc, os, shutil, json
# functions that on kodi 19 moved to xbmcvfs
try:
    import xbmcvfs
    xbmc.translatePath = xbmcvfs.translatePath
    xbmc.validatePath = xbmcvfs.validatePath
    xbmc.makeLegalFilename = xbmcvfs.makeLegalFilename
except:
    pass
from dependencies import platformtools, logger, filetools
from dependencies import config
from threading import Thread
try:
    import urllib.request as urllib
except ImportError:
    import urllib


def run():
    #get platform
    platform_name = str(platform.system())+"-"+str(platform.machine())
    platform_name=platform_name.lower()
    logger.info("platform_name : ",platform_name)
    

    xbmc.executebuiltin("InstallAddon({})".format("pvr.iptvsimple"))
    xbmc.sleep(10000)
    if xbmc.getCondVisibility('System.HasAddon({})'.format("pvr.iptvsimple")):
        xbmc.executebuiltin("RunAddon(plugin.video.lo-scienziato-pazzo)")
    # xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.lo-scienziato-pazzo/default.py)")

if __name__ == "__main__":
    run()