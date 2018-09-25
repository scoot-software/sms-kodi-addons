#
# Author: Scott Ware <scoot.software@gmail.com>
# Copyright (c) 2015 Scott Ware
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

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

    def endJob(self, sid, id):
        response = requests.get(self.settings['serverUrl'] + ':' + self.settings['serverPort']+ '/session/end/' + str(sid) + '/' + str(id), auth=(self.settings['username'], self.settings['password']))

    def addSession(self, id, profile):
        try:
            response = requests.get(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/session/add?id=' + str(id), json=profile, auth=(self.settings['username'], self.settings['password']))
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)
            
    def updateClientProfile(self, id, profile):
        try:
            response = requests.post(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/session/update/' + str(id), json=profile, auth=(self.settings['username'], self.settings['password']))
        except requests.exceptions.RequestException:
            xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    def endSession(self, id):
        response = requests.get(self.settings['serverUrl'] + ':' + self.settings['serverPort'] + '/session/end/' + str(id), auth=(self.settings['username'], self.settings['password']))

def testUrl(settings):
    try:
        response = requests.get(settings['serverUrl'] + ':' + settings['serverPort'] + '/settings/version', auth=(settings['username'], settings['password']), timeout=2.0)
        return True
    except requests.exceptions.RequestException:
        return False
