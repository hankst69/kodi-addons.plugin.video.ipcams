import sys
import os
#import urllib

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
#import xbmcvfs #Matrix


__addon__ = xbmcaddon.Addon()
__addonID__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__path__ = __addon__.getAddonInfo('path')


def paramsToDict(parameters):

    paramDict = {}
    if parameters:
        paramPairs = parameters.split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict


def report(message, level=xbmc.LOGNOTICE, user_message=None):
    xbmc.log('[%s] %s' % (__addonID__, message), level)
    if user_message:
        xbmc.executebuiltin('Notification("%s","%s",)' % (__addonID__, user_message))

arguments = sys.argv

if len(arguments) > 1:
    if arguments[0][0:6] == 'plugin':
        _addonHandle = int(arguments[1])
        arguments.pop(0)
        arguments[1] = arguments[1][1:]

    params = paramsToDict(arguments[1])

    loc_str = __addon__.getLocalizedString(30011)
    report(loc_str)
    loc_str = "Camera %s"

    item = [loc_str % '1', loc_str % '2', loc_str % '3', loc_str % '4']
    cam = [__addon__.getSetting('cam1'), __addon__.getSetting('cam2'), __addon__.getSetting('cam3'), __addon__.getSetting('cam4')]
    loc = [__addon__.getSetting('loc1'), __addon__.getSetting('loc2'), __addon__.getSetting('loc3'), __addon__.getSetting('loc4')]

    #mode = urllib.unquote_plus(params.get('mode', ''))
    #if mode is '':

    cams = 0
    for i in range(int(__addon__.getSetting('numcams'))):

        #Helix-API:
        icon = xbmc.translatePath(os.path.join( __path__,'resources', 'lib', 'media', 'ipcam_%s.png' % (i + 1)))
        #Matrix-API:
        #icon = xbmcvfs.translatePath(os.path.join( __iconpath__, 'ipcam_%s.png' % (i + 1)))

        _listitem = '%s - %s' %(item[i], loc[i])
        if loc[i] == '':
            _listitem = '%s - %s' %(item[i], item[i])
        li = xbmcgui.ListItem(_listitem, iconImage =icon)
        #Matrix-API:
        #li = xbmcgui.ListItem(label=loc[i] if loc[i] != '' else item[i], label2=item[i])
        #icon = xbmcvfs.translatePath(os.path.join( __iconpath__, 'ipcam_%s.png' % (i + 1)))
        #li.setArt({'icon': icon, 'fanart': __fanart__})

        li.setProperty('isPlayable', 'true')
        li.setInfo('video', {'tag': 'Documentary'})

        if cam[i] != '':
            xbmcplugin.addDirectoryItem(_addonHandle, cam[i], li)
            cams += 1
        else:
            break

    if cams > 0:
        xbmcplugin.endOfDirectory(_addonHandle)
    else:
        xbmcgui.Dialog().ok(__addonname__, __addon__.getLocalizedString(30015))
