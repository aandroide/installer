# -*- coding: utf-8 -*-
import io
import platform
import xbmc, os, shutil, json
import subprocess
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
    # platform_name = str(platform.system())+"-"+str(platform.machine())
    # platform_name=platform_name.lower()
    # logger.info("platform_name : ",platform_name)
    

    if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.android'):
        
        # confirmation dialog 
        accept= platformtools.dialog_yesno("Install dependenies","addons need to install iptv client addons, install it?")
        if not accept:
            return
        
        dp = platformtools.dialog_progress_bg(config.get_localized_string(20000),config.get_localized_string(90050) )
        dp.update(0)

        #if respri-pi
        if "arm" in platform.machine().lower():
            pkg1 = subprocess.run(["sudo","apt-get","install","kodi-inputstream-adaptive","-y"])
            dp.update(25)
            pkg2 = subprocess.run(["sudo","apt-get","install","kodi-inputstream-ffmpegdirect","-y"])
            dp.update(50)
            pkg3 = subprocess.run(["sudo","apt-get","install","kodi-inputstream-rtmp","-y"])
            dp.update(75)
            pkg4 = subprocess.run(["sudo","apt-get","install","kodi-pvr-iptvsimple","-y"])
            if pkg1.returncode!=0 or pkg2.returncode!=0 or pkg3.returncode!=0 or pkg4.returncode!=0:
                logger.info("Error in installing")
                platformtools.dialog_ok(config.get_localized_string(20000), config.get_localized_string(90051))
                dp.close()
                return
        
        else: 
            sudo_password=platformtools.dialog_input("", "Enter sudo password:")
            if sudo_password==None:
                platformtools.dialog_ok(config.get_localized_string(20000), "must enter password to install dependencies")
                dp.close()
                return
            output=""
            error=""
            
            try:
                proc= subprocess.Popen(["sudo","apt-get","install","kodi-pvr-iptvsimple","-y"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                output,error= proc.communicate(input=sudo_password+"\n")
            except Exception as ex:
                logger.error(ex)
                platformtools.dialog_ok(config.get_localized_string(20000), "error happen in installation")
                dp.close()
                return
            
            if error != "":
                platformtools.dialog_ok(config.get_localized_string(20000), "error happen in install (internet connection error or wrong password)")
                logger.log("error depe: ","|"+error+"|")

                dp.close()
                return
        
        #after insatllation
        dp.update(95)
        if proc.returncode==0:
            logger.info("installed depenceny success")
            xbmc.sleep(5000)
            xbmc.executebuiltin("UpdateLocalAddons")
            dp.update(100)
            xbmc.executebuiltin("RunAddon(plugin.video.lo-scienziato-pazzo)")
        else:
            logger.info("Error in installing")
            platformtools.dialog_ok(config.get_localized_string(20000), config.get_localized_string(90051))
            dp.close()
            return
        dp.close()
    else:
        xbmc.executebuiltin("InstallAddon({})".format("pvr.iptvsimple"))
        xbmc.sleep(10000)
        xbmc.executebuiltin("UpdateLocalAddons")
        if xbmc.getCondVisibility('System.HasAddon({})'.format("pvr.iptvsimple")):
            xbmc.executebuiltin("RunAddon(plugin.video.lo-scienziato-pazzo)")
    # xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.lo-scienziato-pazzo/default.py)")

# if __name__ == "__main__":
#     logger.log("START INSTALL DEP FROM MAIN...")
#     run()