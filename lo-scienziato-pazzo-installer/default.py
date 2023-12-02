# -*- coding: utf-8 -*-
from dependencies import platformtools
import downloader_service,install_dependency, os, xbmc
# functions that on kodi 19 moved to xbmcvfs
try:
    import xbmcvfs
    xbmc.translatePath = xbmcvfs.translatePath
    xbmc.validatePath = xbmcvfs.validatePath
    xbmc.makeLegalFilename = xbmcvfs.makeLegalFilename
except:
    pass

if os.path.isfile(xbmc.translatePath("special://home/addons/") + "plugin.video.lo-scienziato-pazzo.update.zip"):
    dial = None
    while os.path.isfile(xbmc.translatePath("special://home/addons/") + "plugin.video.lo-scienziato-pazzo.update.zip"):
        if not dial:
            dial = platformtools.dialog_progress('Lo Scienziato Pazzo', 'Attendi che il processo di installazione finisca.')
        xbmc.sleep(500)
        if dial.iscanceled():
            dial.close()
            exit(0)
    dial.close()
    xbmc.executebuiltin("RunAddon(plugin.video.lo-scienziato-pazzo)")
else:
    # Check if the add-on is installed
    is_installed = xbmc.getCondVisibility('System.HasAddon({})'.format("pvr.iptvsimple"))
    if not is_installed:
        install_dependency.run()
    else :
        downloader_service.run()
#update-action