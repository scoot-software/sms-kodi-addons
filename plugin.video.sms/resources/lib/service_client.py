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

import requests

class ServiceClient(object):
    settings = None

    def __init__(self, settings):
        self.settings = settings

    def getSession(self):
        try:
            response = requests.get('http://localhost:' + self.settings['servicePort'] + '/session')
            data = response.text
            return data
        except requests.exceptions.RequestException:
            return None
            
    def update(self):
        try:
            response = requests.get('http://localhost:' + self.settings['servicePort'] + '/update')
            return True
        except requests.exceptions.RequestException:
            return False
