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

class ToolsService(RawsService):

    def __init__(self, username, password, server = None, ssl = False):
        """ Constructor for RassService, used to send request to the RASS service.

        :param username: Name of your Rambla user account
        :param password: Pwd of your Rambla user account
        :param server: Domain name of the TOOLS service. Unless you are and advanced user, use the default (= None).
        :param ssl: Set True to use SSL (your account must be SSL enabled) (optional, default = False)
        """
        self.username = username
        self.server = server
        if server is None:
            self.server = "%s.master.tools.tool01.rambla.be" % self.username
        super(ToolsService, self).__init__(username = username, password = password, server = self.server, ssl = ssl)

    def doCdnPush(self, path):
        """ Method for cdnpush2 resource

            @param path: Filename or relative path of the recorded file, starting from the recording directory.
            @return dictionary object containing at least the 'pushed' key, and optionally also 'encoding_job' and/or 'encoded' data
        """
        uri = "/cdnpush2/" + path.lstrip("/")
        return self.Get(uri = uri)
        
        

