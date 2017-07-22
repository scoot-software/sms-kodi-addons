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
FILES = "3gp,aac,avi,flac,m4a,m4v,mka,mkv,mp3,mp4,mpeg,mpg,oga,ogg,wav,webm,dsf"
CODECS = "h264,hevc,vp8,mpeg2video,vc1,mp3,aac,flac,ac3,vorbis,alac,dts,pcm,dsd,truehd,subrip,webvtt,dvb,dvd,pgs"
MCH_CODECS = "ac3,aac,dts,flac,pcm,dsd,truehd,vorbis"
FORMAT = "hls"

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
	    		response = requests.get(self.settings['serverUrl'] + '/media/recentlyadded/50?type=' + str(type), auth=(self.settings['username'], self.settings['password']))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching recently added media from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

	def getRecentlyPlayedElements(self, type):
		try:
	    		response = requests.get(self.settings['serverUrl'] + '/media/recentlyplayed/50?type=' + str(type), auth=(self.settings['username'], self.settings['password']))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching recently played media from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def getMediaFolders(self):
		try:
	    		response = requests.get(self.settings['serverUrl'] + '/media/folder', auth=(self.settings['username'], self.settings['password']))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching media folders from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def getMediaFolderContents(self, id):
		try:
	    		response = requests.get(self.settings['serverUrl'] + '/media/folder/' + str(id) + '/contents', auth=(self.settings['username'], self.settings['password']))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def getDirectoryElementContents(self, id):
		try:
	    		response = requests.get(self.settings['serverUrl'] + '/media/' + str(id) + '/contents', auth=(self.settings['username'], self.settings['password']))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def getMediaElement(self, id):
		try:
	    		response = requests.get(self.settings['serverUrl'] + '/media/' + str(id), auth=(self.settings['username'], self.settings['password']))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def initialiseStream(self, session, id, type):
		try:
			url = self.settings['serverUrl'] + '/stream/initialise/' + str(session) + '/' + str(id)
			url += '?client=' + CLIENT			
			url += '&files=' + FILES
			url += '&codecs=' + CODECS
			
			if self.settings['multichannel'] == 'true':
				url += '&mchcodecs=' + MCH_CODECS

			url += '&format=' + FORMAT

			if type == 0:
				url += '&quality=' + self.settings['audioQuality']
			elif type == 1:
				url += '&quality=' + self.settings['videoQuality']

			url += '&samplerate=' + self.settings['maxSampleRate']
			url += '&direct=' + self.settings['directPlay']

	    		response = requests.get(url, auth=(self.settings['username'], self.settings['password']))
	    		data = response.json()
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error initialising the stream.', xbmcgui.NOTIFICATION_ERROR, 5000)

    	def endJob(self, id):
		response = requests.get(self.settings['serverUrl'] + '/job/end/' + str(id), auth=(self.settings['username'], self.settings['password']))

	def createSession(self):
		try:
	    		response = requests.get(self.settings['serverUrl'] + '/session/create', auth=(self.settings['username'], self.settings['password']))
	    		data = response.text
	    		return data
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error creating a new session.', xbmcgui.NOTIFICATION_ERROR, 5000)

	def addSession(self, id):
		try:
	    		response = requests.get(self.settings['serverUrl'] + '/session/add/' + str(id), auth=(self.settings['username'], self.settings['password']))
		except requests.exceptions.RequestException:
	    		xbmcgui.Dialog().notification('mediaStreamer', 'There was an error fetching content from the server.', xbmcgui.NOTIFICATION_ERROR, 5000)

	def endSession(self, id):
		response = requests.get(self.settings['serverUrl'] + '/session/end/' + str(id), auth=(self.settings['username'], self.settings['password']))

def testUrl(settings):
	try:
    		response = requests.get(settings['serverUrl'] + '/settings/version', auth=(settings['username'], settings['password']), timeout=2.0)
		return True
	except requests.exceptions.RequestException:
        	return False
