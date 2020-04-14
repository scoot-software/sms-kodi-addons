"""
    Scoot Media Streamer
    Copyright (C) 2020  Scott Ware

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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
