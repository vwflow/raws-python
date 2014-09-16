#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 rambla.eu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.import os
import json, os
import raws_json
from raws_json.raws_service import RawsService, Feed, Query, RequestError

class RaseService(RawsService):

    def __init__(self, username, password, server, ssl = False):
        """ Constructor for RassService, used to send request to the RASS service.

        :param username: Name of your Rambla user account
        :param password: Pwd of your Rambla user account
        :param server: Domain name of the RASS service (either 'rass.cdn01.rambla.be' or 'rass.cdn02.rambla.be', depending on the subCDN you're using)
        :param ssl: Set True to use SSL (your account must be SSL enabled) (optional, default = False)
        """
        self.username = username
        super(RaseService, self).__init__(username = username, password = password, server = server, ssl = ssl)

    def delete(self, uri):
        """ Deletes any resource, given the uri. """
        return self.Delete(uri = uri)


    def setTransrate(self, user, top_format, formats):
        """ Tries to POST a new vocab resource to META, in order to update the entry that was passed as argument.

            @param dict The (modified) vocab entry dict, that will be posted to META.
            @return Vocab entry dict
        """
        entry = {"entry":{"content":{ "params": {"user": user, "top_format": top_format,}, "formats" : formats},},}
        uri = "/transrate/" + user + "/"
        print entry
        print uri
        return self.Post(entry, uri= uri)

    def getWowapps(self, query = None):
        """ Retrieves a total feed. 

            @return Wowapp feed object
        """
        uri = "/wowapp/"
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Get(uri = uri)

    def getMpegts(self, uri):
        """ Retrieves a Mpegts instance or list (depending on the URI). 

            @param uri GET Mpegts URL for your user account.
            @return List of Mpegts dicts or Mpegts entry dict
        """
        return self.Get(uri = uri)
