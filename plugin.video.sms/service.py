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
import os
import sys
import urllib
import urlparse
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

################################################################################################

if __name__ == '__main__':
    	# Settings
	sms_settings = {\
			'serverUrl': addon.getSetting('serverUrl') + ':' + addon.getSetting('serverPort'), \
			'username': addon.getSetting('username'), \
			'password': addon.getSetting('password'), \
			'servicePort': addon.getSetting('servicePort')}

    	# REST Client
    	sms_client = client.RESTClient(sms_settings)

	# Main loop
	monitor = xbmc.Monitor()
 
	while not monitor.abortRequested():
		# Sleep/wait for abort for 10 seconds
		if monitor.waitForAbort(10):
			# Abort was requested while waiting. We should exit
			break

