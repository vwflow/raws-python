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

class RatsService(RawsService):
    
    ENCODE_MP4_480P_WITH_SNAPSHOTS = "1"  # Encode to mp4 (for online viewing) with same dimensions + make snapshots
    EXPORT_TO_CDN = "1"                 # Export encoded files to your CDN account
    
    MAIL_CDN_REPORT = "13"              # Mail CDN report in JSON format
    POST_CDN_REPORT = "14"              # Send CDN report as body of HTPP POST request (URL must be specified in client_input param)
    MAIL_HUMAN_READABLE = "24"          # Send a human readable mail with info about encoding + published files

    # Jon status codes
    JOB_RECEIVED = 1
    JOB_IMPORTING = 2
    JOB_IMPORTED = 3
    JOB_TRANSCODING = 4
    JOB_TRANSCODED = 5
    JOB_EXPORTING = 6
    JOB_SUCCEEDED = 7                   # if status >= 7: job has finished
    JOB_IMPORT_FAILED = 8
    JOB_TRANSCODING_FAILED = 9
    JOB_EXPORT_FAILED = 10
    
    def __init__(self, username, password, server=None, ssl = False):
        """ Constructor for RatsService, used to send request to the RATS service.

        :param username: Name of your Rambla user account
        :param password: Pwd of your Rambla user account
        :param server: Domain name of the RATS service (optional, default = "rats.enc01.rambla.be")
        :param ssl: Set True to use SSL (your account must be SSL enabled) (optional, default = False)
        """
        self.username = username
        if server is None:
            server = "rats.enc01.rambla.be"
        super(RatsService, self).__init__(username = username, password = password, server = server, ssl = ssl)

    def delete(self, uri):
        """ Deletes any resource, given the uri. """
        return self.Delete(uri = uri)

    def createSrc(self, filename, local_path):
        """ Tries to PUT a new src resource to RATS.

            @param filename filename to be given to the uploaded file on the RATS server.
            @param local_path location of the file to be uploaded on the local machine

            @return SrcEntry object
        """
        media_source = raws_json.MediaSource(file_path = local_path, svr_filename = filename)
        media_entry = self.Put(data = None, uri = '/src/', media_source = media_source)
        return media_entry

    def createJob(self, input=None, output=None, format=None, formatgroup = None, src_location=None, import_location=None, tgt_location=None, startpos=None, endpos=None, 
                    client_passthru=None, client_input=None, proc = None, snapshot_interval = None):
        """ Tries to POST a new input resource to RATS, containing the params that were passed as string args.

            Use src_location if the src is already available on the RATS server.
            Use import_location if the src still needs to be imported.

            @return JobEntry object
        """
        params = {}

        if format and formatgroup:
            raise Exception("Invalid parameters passed to createJob(): both format and formatgroup were set. These can not be combined!")
        if format:
            params["format"] = format
        elif formatgroup:
            params["formatgroup"] = formatgroup
        else:
            raise Exception("Invalid parameters passed to createJob(): can't create a job without a format or formatgroup ID.")

        if src_location and import_location:
            raise Exception("Invalid parameters passed to createJob(): both format and input_location were set. These can not be combined!")
        if src_location:
            params["src_location"] = src_location
        elif import_location:
            params["import_location"] = import_location
        else:
            raise Exception("Invalid parameters passed to createJob(): can't create a job without a src_location or input_location.")
        
        if input:
            params["input"] = input
        if output:
            params["output"] = output
        if tgt_location:
            params["tgt_location"] = tgt_location
        if startpos:
            params["startpos"] = startpos
        if endpos:
            params["endpos"] = endpos
        if client_passthru:
            params["client_passthru"] = client_passthru
        if client_input:
            params["client_input"] = client_input
        if proc:
            params["proc"] = proc
        if snapshot_interval:
            params["snapshot_interval"] = snapshot_interval
            
        entry = {"entry":{"content":{"params":params},},}
        uri = "/job/"
        return self.Post(entry, uri= uri)
        
    def getJob(self, uri):
        """ Retrieves a job entry. 

            @param uri path (relative or absolute) to the job instance.
            @return JobEntry object
        """
        if uri is None:
            raise Exception('You must provide a valid URI argument to getJob().')
        return self.Get(uri)
