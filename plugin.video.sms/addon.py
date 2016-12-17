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
import sms

################################################################################################

addon = xbmcaddon.Addon('plugin.video.sms')
addon_path = addon.getAddonInfo('path').decode('utf-8')

################################################################################################

#
# Helper Functions
#

def buildUrl(query):
    	return baseUrl + '?' + urllib.urlencode(query)

def mainMenu():
	# Media Browser
	url = buildUrl({'url': sms_client.settings.serverUrl, 'mode': 'media_browser'})
        item = xbmcgui.ListItem('Media Browser',iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addonHandle,
                		    url=url,
                		    listitem=item,
                		    isFolder=True)

	# Recently Played
	url = buildUrl({'url': sms_client.settings.serverUrl, 'mode': 'recently_played'})
        item = xbmcgui.ListItem('Recently Played',iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addonHandle,
                		    url=url,
                		    listitem=item,
                		    isFolder=True)

	# Recently Added
	url = buildUrl({'url': sms_client.settings.serverUrl, 'mode': 'recently_added'})
        item = xbmcgui.ListItem('Recently Added',iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addonHandle,
                		    url=url,
                		    listitem=item,
                		    isFolder=True)

	xbmcplugin.endOfDirectory(addonHandle)

def mediaFolders():
    	folders = sms_client.getMediaFolders()
    	total = len(folders)

    	for folder in folders:
            	if folder['type'] == 1:
            		url = buildUrl({'url': sms_client.settings.serverUrl, 'mode': 'media_folder','id': folder['id']})
            		item = xbmcgui.ListItem(folder['name'],iconImage='DefaultFolder.png')
            		xbmcplugin.addDirectoryItem(
                		handle=addonHandle,
                		url=url,
                		listitem=item,
                		isFolder=True)

    	xbmcplugin.endOfDirectory(addonHandle)

def recentlyPlayedList():
	elements = sms_client.getRecentlyPlayedVideoElements()
	parseMediaElements(elements, True)

def recentlyAddedList():
	elements = sms_client.getRecentlyAddedVideoElements()
	parseMediaElements(elements, True)

def mediaFolderContents():
    	elements = sms_client.getMediaFolderContents(arguments.get('id', None)[0])
    	parseMediaElements(elements, False)
	
def directoryElementContents():
    	elements = sms_client.getDirectoryElementContents(arguments.get('id', None)[0])
    	parseMediaElements(elements, False)
    
def parseMediaElements(elements, altTitle):
    	total = len(elements)

    	for element in elements:
		elementType = element['type']

		# Process Title
		title = element['title']

		if altTitle and 'collection' in element:
			if not element['collection'] in element['title']:
				title = element['collection'] + ' - ' + element['title']
				

        	if elementType == 1:
	    		url = buildUrl({'url': sms_client.settings.serverUrl, 'mode': 'video_element','id': element['id']})
			item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png')
			item.setContentLookup(0)
			item.setProperty("IsPlayable", "true")
			item.setInfo('video', { 'title': element['title'] })
			    
			if 'rating' in element:
				item.setInfo('video', { 'rating': element['rating'] })

			if 'tagline' in element:
				item.setInfo('video', { 'tagline': element['tagline'] })

			if 'description' in element:
				item.setInfo('video', { 'plot': element['description'] })
			    
			if 'certificate' in element:
				item.setInfo('video', { 'mpaa': element['certificate'] })

			if 'year' in element:
				item.setInfo('video', { 'year': element['year'] })

			if 'genre' in element:
				item.setInfo('video', { 'genre': element['genre'] })

			if 'collection' in element:
				item.setInfo('video', { 'set': element['collection'] })
			
			if 'duration' in element:
				if sms.utils.getVersion() < 15:
				    	item.setInfo('video', { 'duration': element['duration'] // 60})
				else:
				    	item.setInfo('video', { 'duration': element['duration'] })

			item.setArt({ 'thumb': sms_settings.serverUrl + '/image/' + str(element['id']) + '/thumbnail/500', 'poster': sms_settings.serverUrl + '/image/' + str(element['id']) + '/cover/500', 'fanart' : sms_settings.serverUrl + '/image/' + str(element['id']) + '/fanart/' + str(xbmcgui.Window().getWidth()) })

			xbmcplugin.addDirectoryItem(
				handle=addonHandle,
				url=url,
				listitem=item)

        	elif elementType == 2:
		    	directoryType = element['directoryType']

			if directoryType >= 1:
				url = buildUrl({'url': sms_client.settings.serverUrl, 'mode': 'directory_element','id': element['id']})
				item = xbmcgui.ListItem(title,iconImage='DefaultFolder.png')
				item.setProperty("IsPlayable", "false")
				item.setInfo('video', { 'title': element['title'] })
					
				if directoryType == 1:
					if 'year' in element:
						item.setInfo('video', { 'year': str(element['year']) })
			
					if 'rating' in element:
						item.setInfo('video', { 'rating': element['rating'] })

					if 'tagline' in element:
						item.setInfo('video', { 'tagline': element['tagline'] })

					if 'description' in element:
						item.setInfo('video', { 'plot': element['description'] })

					if 'certificate' in element:
						item.setInfo('video', { 'mpaa': element['certificate'] })

					if 'genre' in element:
						item.setInfo('video', { 'genre': element['genre'] })

					if 'collection' in element:
						item.setInfo('video', { 'set': element['collection'] })

				item.setArt({ 'poster': sms_settings.serverUrl + '/image/' + str(element['id']) + '/cover/500', 'fanart' : sms_settings.serverUrl + '/image/' + str(element['id']) + '/fanart/' + str(xbmcgui.Window().getWidth()) })

				xbmcplugin.addDirectoryItem(
					handle=addonHandle,
					url=url,
					listitem=item,
					isFolder=True)

    	xbmcplugin.endOfDirectory(addonHandle)

def playVideo():
    	id = arguments.get('id', None)[0]
    	profile = sms_client.initialiseStream(id, 1)
    	element = sms_client.getMediaElement(id)
    	url = sms_settings.serverUrl + '/stream/' + str(profile['id'])

    	item = xbmcgui.ListItem(element['title'], path=url, iconImage="DefaultVideo.png")
	item.setArt({ 'thumb': sms_settings.serverUrl + '/image/' + str(element['id']) + '/thumbnail/500', 'poster': sms_settings.serverUrl + '/image/' + str(element['id']) + '/cover/500', 'fanart' : sms_settings.serverUrl + '/image/' + str(element['id']) + '/fanart/' + str(xbmcgui.Window().getWidth()) })
    	item.setInfo('video', { 'title': element['title'] })
	item.setMimeType(profile['mimeType'])
	item.setContentLookup(0)

    	if 'rating' in element:
        	item.setInfo('video', { 'rating': element['rating'] })

    	if 'tagline' in element:
        	item.setInfo('video', { 'tagline': element['tagline'] })

    	if 'description' in element:
        	item.setInfo('video', { 'plot': element['description'] })
	    
    	if 'certificate' in element:
        	item.setInfo('video', { 'mpaa': element['certificate'] })

    	if 'year' in element:
        	item.setInfo('video', { 'year': element['year'] })

   	if 'genre' in element:
       	 	item.setInfo('video', { 'genre': element['genre'] })

	if 'collection' in element:
		item.setInfo('video', { 'set': element['collection'] })

    	if 'duration' in element:
		if sms.utils.getVersion() < 15:
	   		item.setInfo('video', { 'duration': element['duration'] // 60})
		else:
	    		item.setInfo('video', { 'duration': element['duration'] })

    	xbmcplugin.setResolvedUrl(handle=addonHandle, succeeded=True, listitem=item)

	# Blocking call to monitor playback
	sms.player.monitorPlayback(url, addonUrl)

    	# End job
    	sms_client.endJob(profile['id'])

    	return

#
# Main Plugin Navigation
#

if __name__ == '__main__':
    	# Settings
	sms_settings = sms.client.Settings(addon.getSetting('sms_url'), \
				      addon.getSetting('username'), \
				      addon.getSetting('password'), \
				      addon.getSetting('videoquality')[:1], \
				      addon.getSetting('maxsamplerate'), \
				      addon.getSetting('multichannel'), \
				      addon.getSetting('directplay'))

	# XBMC Plugin URLs
    	addonUrl = sys.argv[0] + sys.argv[2]
	baseUrl = sys.argv[0]
    	addonHandle = int(sys.argv[1])
    	arguments = urlparse.parse_qs(sys.argv[2][1:])

    	# REST Client
    	sms_client = sms.client.RESTClient(sms_settings)

    	# Test connection with server
    	if not sms_client.testConnection():
		dialog = xbmcgui.Dialog().ok('Scoot Media Streamer', 'Unable to connect to server. Please check that the plugin settings are correct.')
	
		if dialog:
	    		addon.openSettings()
	    		sys.exit("Settings incorrect.")
		else:
	    		sys.exit("Settings incorrect.")

    	# Addon Routing
    	mode = arguments.get('mode', None)

    	if mode is None:
        	mainMenu()
	elif mode[0] == 'media_browser':
        	mediaFolders()
	elif mode[0] == 'recently_played':
        	recentlyPlayedList()
	elif mode[0] == 'recently_added':
        	recentlyAddedList()
    	elif mode[0] == 'media_folder':
        	mediaFolderContents()
    	elif mode[0] == 'directory_element':
        	directoryElementContents()
    	elif mode[0] == 'video_element':
		playVideo()
