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

# ReplayGain mapping
replaygain = {0:0, 1:2, 2:1}

class ClientProfile:
    
    def __init__(self, client, format, formats, codecs, mchCodecs, videoQuality, audioQuality, maxBitrate, maxSampleRate, replaygain, directPlay):
        self.client = client
        self.format = format
        self.formats = formats
        self.codecs = codecs
        self.mchCodecs = mchCodecs
        self.videoQuality = videoQuality
        self.audioQuality = audioQuality
        self.maxBitrate = maxBitrate
        self.maxSampleRate = maxSampleRate
        self.replaygain = replaygain
        self.directPlay = directPlay
