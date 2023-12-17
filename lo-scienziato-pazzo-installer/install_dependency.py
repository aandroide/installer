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


def install_depenecy(pkg_name,dist="ubuntu"):
    if dist == "arch":
        pkg = subprocess.run(["sudo","yaourt","install",pkg_name,"-y"])
    else:
        pkg = subprocess.run(["sudo","apt-get","install",pkg_name,"-y"])
    return pkg        

def install_depenency_with_sudo(pkg_name,sudo_password,dist="ubuntu"):
    if dist == "arch":
        proc= subprocess.Popen(["sudo","yaourt","-S","install",pkg_name,"-y"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    else:
        proc= subprocess.Popen(["sudo","apt-get","-S","install",pkg_name,"-y"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    
    output,error=proc.communicate(input=sudo_password+"\n")
    return proc
          

def check_sudo_password():      
    try:
        result = subprocess.check_output('sudo -n true 1',shell=True)
        return 0
    except:
        return 1

def ask_for_password():
    sudo_password=platformtools.dialog_input("", config.get_localized_string(90053))
    if sudo_password==None:
        platformtools.dialog_ok(config.get_localized_string(20000), config.get_localized_string(90054))
    
    return sudo_password


def linux_distro():
    try:
        import distro
        return distro.id()
    except:
        return "N/A"
        
def get_platform():

    if xbmc.getCondVisibility('system.platform.osx'):
        return "OSX"
    elif xbmc.getCondVisibility('System.HasAddon(service.coreelec.settings)'):
        return "CoreElec"
    elif xbmc.getCondVisibility('System.HasAddon(service.libreelec.settings)'):
        return "LibreElec"
    elif xbmc.getCondVisibility('System.HasAddon(service.osmc.settings)'):
        return "OSMC"
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return "ATV2"
    elif xbmc.getCondVisibility('system.platform.ios'):
        return "iOS"
    elif xbmc.getCondVisibility('system.platform.windows'):
        return platform.platform(terse=True)
    elif xbmc.getCondVisibility('system.platform.android'):
        return "Android"
    elif os.path.exists('/usr/share/plasma/desktoptheme/kubuntu'):
        if "Ubuntu" in os.uname()[3]:
          return "Kubuntu"
    elif xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.android'):
        print("Detected OS: Linux")
        with open ('/sys/firmware/devicetree/base/model') as model:
          RPi_model=model.read()
          return RPi_model
        if "Ubuntu" in os.uname()[3]:
          return "Ubuntu"
    else:
        return "Unknown"
        
def success_installation(dp):
    logger.info("installed dependencies success")
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.sleep(1000)
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled", "params":{"addonid":"pvr.iptvsimple", "enabled": "toggle"},"id":1}')
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled", "params":{"addonid":"kodi.inputstream.adaptive", "enabled": "toggle"},"id":1}')
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled", "params":{"addonid":"kodi.inputstream.ffmpegdirect", "enabled": "toggle"},"id":1}')
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled", "params":{"addonid":"kodi.inputstream.rtmp", "enabled": "toggle"},"id":1}')
    platformtools.dialog_ok(config.get_localized_string(20000), config.get_localized_string(90057))
    dp.update(100)
    dp.close() 
    platformtools.dialog_ok(config.get_localized_string(20000), config.get_localized_string(90052))
    xbmc.sleep(1000)
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.lo-scienziato-pazzo/default.py)")    
        
def failed_installation(dp):
    logger.info("Error in installing")
    dp.close()
    platformtools.dialog_ok(config.get_localized_string(20000), config.get_localized_string(90051))

def install_libre():
    if get_platform()=="LibreElec": 
        xbmc.executebuiltin("InstallAddon({})".format("pvr.iptvsimple"))    
        xbmc.sleep(10000)
        xbmc.executebuiltin("UpdateLocalAddons")
        tries=0
        while tries<30000 and not xbmc.getCondVisibility('System.HasAddon({})'.format("pvr.iptvsimple")):
            xbmc.sleep(500)
            tries= tries+500
        
        if xbmc.getCondVisibility('System.HasAddon({})'.format("pvr.iptvsimple")):
            xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.lo-scienziato-pazzo/default.py)")

def install_dep_in_linux():
    # confirmation dialog 
    accept= platformtools.dialog_yesno(config.get_localized_string(90055),config.get_localized_string(90056))
    if not accept:
        return
    dp = platformtools.dialog_progress_bg(config.get_localized_string(20000),config.get_localized_string(90050))
    dp.update(0)
    
    #Check sudo password 
    sudo_password=""
    password_needed=check_sudo_password()
    dp.update(10)
    xbmc.sleep(1000)

    #if password needes ask
    if password_needed:
        sudo_password=ask_for_password()
        if sudo_password==None:
            dp.close()
            return    

    
    # installation
    try:
        success=0 
        # if arch    
        if linux_distro()=="arch":
            proc= subprocess.Popen(["sudo","-S","yaourt","install","kodi-addon-pvr-iptvsimple","-y"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding="utf-8")
            output,error= proc.communicate(input=sudo_password+"\n")
            if proc.returncode==0: success=1
                
        # if it's rasperry-pi 
        elif "arm" in platform.machine().lower():
            pkg1 = install_depenecy("kodi-inputstream-adaptive")
            dp.update(25)
            pkg2 = install_depenecy("kodi-inputstream-ffmpegdirect")
            dp.update(50)
            pkg3 = install_depenecy("kodi-inputstream-rtmp")
            dp.update(75)
            pkg4 = install_depenecy("kodi-pvr-iptvsimple")

            if pkg1.returncode==0 and pkg2.returncode==0 and pkg3.returncode==0 and pkg4.returncode==0:
                success=1
        #if it's ubuntu
        else:
            proc= subprocess.Popen(["sudo","-S","apt-get","install","kodi-pvr-iptvsimple","-y"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding="utf-8")
            output,error= proc.communicate(input=sudo_password+"\n")
            if proc.returncode==0: success=1
            
            

        ################################
        # check installation
        ###############################
        dp.update(95)
        if success==1:success_installation(dp)
        else : failed_installation(dp)   
        
        dp.close()               
    except Exception as ex:
        logger.info("Error in installing",ex)
        platformtools.dialog_ok(config.get_localized_string(20000), config.get_localized_string(90051))
        dp.close()

def run():

    # new function platform 
    logger.info("Stai utilizzando:", get_platform())
    
    platformtools.dialog_ok(config.get_localized_string(90058), get_platform())

    if get_platform()=="LibreElec":
        install_libre()

    # --- if linux ---
    #if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.android'):
    elif get_platform()=="Ubuntu":
        install_dep_in_linux()
        
    elif get_platform()=="Kubuntu":
        install_dep_in_linux()

    elif get_platform()=="Raspberry":
        install_dep_in_linux()
        
    else:#--- if not linux --- 
        xbmc.executebuiltin("InstallAddon({})".format("pvr.iptvsimple"))
        xbmc.sleep(10000)
        xbmc.executebuiltin("UpdateLocalAddons")
        
        tries=0
        while tries<30000 and not xbmc.getCondVisibility('System.HasAddon({})'.format("pvr.iptvsimple")):
            xbmc.sleep(500)
            tries= tries+500
        
        if xbmc.getCondVisibility('System.HasAddon({})'.format("pvr.iptvsimple")):
            xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.lo-scienziato-pazzo/default.py)")
        
# if __name__ == "__main__":
#     logger.log("START INSTALL DEP FROM MAIN...")
#     run()
