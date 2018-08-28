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
################################################################################################

from operator import itemgetter
from bottle import route, run
from threading import Thread
import os
import sys
import urllib
import urlparse
import requests
import time
import uuid
import json
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

################################################################################################

addon = xbmcaddon.Addon('plugin.video.sms')
addon_path = addon.getAddonInfo('path').decode('utf-8')
libs = xbmc.translatePath(os.path.join(addon_path, 'resources', 'lib')).decode('utf-8')
sys.path.append(libs)

################################################################################################

import sms
import client
import bottle_ext

################################################################################################

CLIENT = 4
FORMATS = [1,2,3,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
CODECS = [10,11,12,13,20,30,31,32,40,1000,1001,1002,1003,1004,1005,1006,1007,1009,1010,1011,2000,2001,2002,2003,2004]
MCH_CODECS = [1000,1001,1002,1003,1004,1005,1006,1009,1010,1011]
FORMAT = 9

class Service(object):

    settings = None
    serverClient = None
    sessionId = None
    clientProfile = None
    controller = None
    server = None
    monitor = None

    def start(self):
        # Settings
        self.settings = {\
            'serverUrl': addon.getSetting('serverUrl') + ':' + addon.getSetting('serverPort'), \
            'username': addon.getSetting('username'), \
            'password': addon.getSetting('password'), \
            'audioQuality': addon.getSetting('audioQuality')[:1], \
            'videoQuality': addon.getSetting('videoQuality')[:1], \
            'maxSampleRate': addon.getSetting('maxSampleRate'), \
            'multichannel': addon.getSetting('multichannel'), \
            'directPlay': addon.getSetting('directPlay'),
            'servicePort': addon.getSetting('servicePort')}

        # SMS Server Client
        self.serverClient = client.RESTClient(self.settings)

        # Session ID
        self.sessionId = uuid.uuid4()
        
        # Client Profile
        self.clientProfile = sms.ClientProfile(CLIENT, FORMAT, FORMATS, CODECS, None, self.settings['videoQuality'], self.settings['audioQuality'], 0, self.settings['maxSampleRate'], self.settings['directPlay'])
        
        if self.settings['multichannel'] == 'true':
            self.clientProfile.mchCodecs = MCH_CODECS
        
        self.serverClient.addSession(self.sessionId, self.clientProfile.__dict__)

        # REST Service
        @route('/session')
        def getSession():
            return str(self.sessionId)
            
        self.server = bottle_ext.WSGIServer(host='localhost', port=self.settings['servicePort'])
        Thread(target=self.rest).start()

        # Main loop
        self.monitor = xbmc.Monitor()
     
        while not self.monitor.abortRequested():
            if self.monitor.waitForAbort(1):
                # Abort was requested while waiting.
                self.shutdown()
                break
    
    def shutdown(self):
        self.serverClient.endSession(self.sessionId)
        self.server.shutdown()
        
    def rest(self):
        run(server=self.server)

if __name__ == '__main__':
    service = Service()
    service.start()

