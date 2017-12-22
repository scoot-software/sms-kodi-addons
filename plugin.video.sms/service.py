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
from bottle import Bottle, ServerAdapter, run
import os
import sys
import urllib
import urlparse
import requests
import time
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

import client
import uuid

################################################################################################

class Service(object):

    settings = None
    serverClient = None
    sessionId = None
    controller = None
    monitor = None

    def start(self):
        # Settings
        self.settings = {\
            'serverUrl': addon.getSetting('serverUrl') + ':' + addon.getSetting('serverPort'), \
            'username': addon.getSetting('username'), \
            'password': addon.getSetting('password'), \
            'servicePort': addon.getSetting('servicePort')}

        # SMS Server Client
        self.serverClient = client.RESTClient(self.settings)

        # Session ID
        self.sessionId = uuid.uuid4()
        self.serverClient.addSession(self.sessionId)

        # REST Service
        self.controller = Bottle()

        @self.controller.route('/session')
        def getSession():
            return str(self.sessionId)

        run(self.controller, host='localhost', port=self.settings['servicePort'])

        # Main loop
        self.monitor = xbmc.Monitor()
     
        while not self.monitor.abortRequested():
            if self.monitor.waitForAbort(1):
                # Abort was requested while waiting.
                self.shutdown()
                break


    def shutdown(self):
        self.serverClient.endSession(self.sessionId)

if __name__ == '__main__':
    service = Service()
    service.start()

