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

CLIENT = "kodi"
FILES = "3gp,aac,avi,flac,m4a,m4v,mka,mkv,mp3,mp4,mpeg,mpg,oga,ogg,wav,webm"
CODECS = "h264,vp8,mpeg2video,vc1,mp3,aac,flac,ac3,vorbis,alac,dts,pcm,truehd,subrip,dvb,dvd,pgs"
MCH_CODECS = "ac3,aac,dts,flac,pcm,truehd,vorbis"
FORMAT = "hls"

class Settings(object):
	serverUrl = None
    	username = None
    	password = None
    	quality = None
    	maxSampleRate = None
    	multichannel = None
	directPlay = None

	def __init__(self, \
		     serverUrl, \
		     username, \
		     password, \
		     quality, \
		     maxSampleRate, \
		     multichannel, \
	             directPlay):

		self.serverUrl = serverUrl
        	self.username = username
        	self.password = password
		self.quality = quality
		self.maxSampleRate = maxSampleRate
		self.multichannel = multichannel
		self.directPlay = directPlay

class RESTClient(object):
	settings = None

    	def __init__(self, settings):
        	self.settings = settings

    	def testConnection(self):
		if testUrl(self.settings.serverUrl, self.settings.username, self.settings.password):
			return True

		return False

	def getRecentlyAddedVideoElements(self):
		try:
	    		response = requests.get(self.settings.serverUrl + '/media/recentlyadded/50?type=1', auth=(self.settings.username, self.settings.password))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching recently added media from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

	def getRecentlyPlayedVideoElements(self):
		try:
	    		response = requests.get(self.settings.serverUrl + '/media/recentlyplayed/50?type=1', auth=(self.settings.username, self.settings.password))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching recently played media from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

	def getRecentlyAddedAudioElements(self):
		try:
	    		response = requests.get(self.settings.serverUrl + '/media/recentlyadded/50?type=0', auth=(self.settings.username, self.settings.password))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching recently added media from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

	def getRecentlyPlayedAudioElements(self):
		try:
	    		response = requests.get(self.settings.serverUrl + '/media/recentlyplayed/50?type=0', auth=(self.settings.username, self.settings.password))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching recently played media from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def getMediaFolders(self):
		try:
	    		response = requests.get(self.settings.serverUrl + '/media/folder', auth=(self.settings.username, self.settings.password))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching media folders from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def getMediaFolderContents(self, id):
		try:
	    		response = requests.get(self.settings.serverUrl + '/media/folder/' + str(id) + '/contents', auth=(self.settings.username, self.settings.password))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def getDirectoryElementContents(self, id):
		try:
	    		response = requests.get(self.settings.serverUrl + '/media/' + str(id) + '/contents', auth=(self.settings.username,self.settings.password))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def getMediaElement(self, id):
		try:
	    		response = requests.get(self.settings.serverUrl + '/media/' + str(id), auth=(self.settings.username, self.settings.password))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def initialiseStream(self, id, type):
		try:
			url = self.settings.serverUrl + '/stream/initialise/' + str(id)
			url += '?client=' + CLIENT			
			url += '&files=' + FILES
			url += '&codecs=' + CODECS
			
			if self.settings.multichannel == 'true':
				url += '&mchcodecs=' + MCH_CODECS

			url += '&format=' + FORMAT
			url += '&quality=' + self.settings.quality
			url += '&samplerate=' + self.settings.maxSampleRate
			url += '&direct=' + self.settings.directPlay

	    		response = requests.get(url, auth=(self.settings.username, self.settings.password))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error initialising the stream.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def endJob(self, id):
		response = requests.get(self.settings.serverUrl + '/job/end/' + str(id), auth=(self.settings.username, self.settings.password))

def testUrl(url, username, password):
	try:
    		response = requests.get(url + '/settings/version', auth=(username, password), timeout=2.0)
		return True
	except requests.exceptions.RequestException:
        	return False
