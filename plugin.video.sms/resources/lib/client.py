"""
    Copyright (C) 2020 Scott Ware
    This file is part of Scoot Media Streamer (plugin.video.sms)
    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
"""

import requests
import xbmcgui

class RESTClient(object):
    settings = None

    def __init__(self, settings):
        self.settings = settings

    def testConnection(self):
        if testUrl(self.settings):
            return True

        return False

    def getRecentlyAddedElements(self, type):
        try:
            response = requests.get(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/media/recentlyadded/50?type=' + str(type), auth=(self.settings['username'], self.settings['password']))
            data = response.json()
            return data
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching recently added media from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    def getRecentlyPlayedElements(self, type):
        try:
            response = requests.get(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/media/recentlyplayed/50?type=' + str(type), auth=(self.settings['username'], self.settings['password']))
            data = response.json()
            return data
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching recently played media from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    def getMediaFolders(self):
        try:
            response = requests.get(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/media/folder', auth=(self.settings['username'], self.settings['password']))
            data = response.json()
            return data
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching media folders from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    def getMediaFolderContents(self, id):
        try:
            response = requests.get(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/media/folder/' + str(id) + '/contents', auth=(self.settings['username'], self.settings['password']))
            data = response.json()
            return data
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    def getDirectoryElementContents(self, id):
        try:
            response = requests.get(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/media/' + str(id) + '/contents', auth=(self.settings['username'], self.settings['password']))
            data = response.json()
            return data
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    def getMediaElement(self, id):
        try:
            response = requests.get(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/media/' + str(id), auth=(self.settings['username'], self.settings['password']))
            data = response.json()
            return data
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    def getPlaylists(self):
        try:
            response = requests.get(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/playlist', auth=(self.settings['username'], self.settings['password']))
            data = response.json()
            return data
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching playlists from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)
            
    def getPlaylistContents(self, id):
        try:
            response = requests.get(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/playlist/' + str(id) + '/contents', auth=(self.settings['username'], self.settings['password']))
            data = response.json()
            return data
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)
    
    def endJob(self, sid, id):
        response = requests.delete(self.settings['serverUrl'] + ':' + self.settings['serverPort']+ '/session/end/' + str(sid) + '/' + str(id), auth=(self.settings['username'], self.settings['password']))

    def addSession(self, id, profile):
        try:
            response = requests.post(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/session/add?id=' + str(id), json=profile, auth=(self.settings['username'], self.settings['password']))
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)
            
    def updateClientProfile(self, id, profile):
        try:
            response = requests.post(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/session/update/' + str(id), json=profile, auth=(self.settings['username'], self.settings['password']))
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    def endSession(self, id):
        response = requests.delete(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/session/end/' + str(id), auth=(self.settings['username'], self.settings['password']))

def testUrl(settings):
    try:
        response = requests.get(settings['serverUrl'] + ':' + settings['serverPort'] + '/settings/version', auth=(settings['username'], settings['password']), timeout=2.0)
        return True
    except requests.exceptions.RequestException:
        return False
