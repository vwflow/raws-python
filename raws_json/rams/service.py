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
from raws_json.raws_service import RawsService

class RamsService(RawsService):
    
    def __init__(self, username, password, server=None, ssl = True):
        """ Constructor for RamsService, used to send request to the RATS service.

        :param username: Name of your Rambla user account
        :param password: Pwd of your Rambla user account
        :param server: Domain name of the RATS service (optional, default = "rams.enc01.rambla.be")
        :param ssl: Set True to use SSL (your account must be SSL enabled) (optional, default = False)
        """
        self.username = username
        if server is None:
            server = "rams.mon01.rambla.be"
        super(RamsService, self).__init__(username = username, password = password, server = server, ssl = ssl)

    def delete(self, uri):
        """ Deletes any resource, given the uri. """
        return self.Delete(uri = uri)

    def getTotal(self, query = None):
        """ Retrieves a total feed. 

            @return JobEntry object
        """
        uri = "/total/"
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Get(uri = uri)

    def getTraffic(self, query = None):
        """ Retrieves a total feed. 

            @return JobEntry object
        """
        uri = "/traffic/"
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Get(uri = uri)

    def getStorage(self, query = None):
        """ Retrieves a total feed. 

            @return JobEntry object
        """
        uri = "/storage/"
        if query:
            query.feed = uri
            uri = query.ToUri()
        return self.Get(uri = uri)
