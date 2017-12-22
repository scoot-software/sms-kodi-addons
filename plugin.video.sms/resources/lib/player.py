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

import xbmc

class SMSPlayer(xbmc.Player):
    ended = False

    def __init__(self, *args):
        xbmc.Player.__init__(self)
        
    def onPlayBackEnded(self):
        self.ended = True

    def onPlayBackStopped(self):
        self.ended = True

def monitorPlayback(url, addonUrl):
    monitor = xbmc.Monitor()
    player = SMSPlayer()

    xbmc.log(msg='URL: ' + url, level=xbmc.LOGDEBUG);
    xbmc.log(msg='Addon URL: ' + addonUrl, level=xbmc.LOGDEBUG);

    count = 0
    currentFile = None
    playbackStarted = False

    while not monitor.abortRequested():
        if xbmc.Player().isPlaying():
            currentFile = xbmc.Player().getPlayingFile()
            
            xbmc.log(msg='Current File: ' + currentFile, level=xbmc.LOGDEBUG);

            if (currentFile == url) or (currentFile == addonUrl):
                playbackStarted = True
            else:
                if playbackStarted:
                    return
                
                count = count + 1

        if player.ended:
            return

        if count > 4:
            return

        if monitor.waitForAbort(5):
            return
