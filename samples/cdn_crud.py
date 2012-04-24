#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2012 rambla.eu
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
# limitations under the License.

""" This sample demonstrates how to manage files and directories on the CDN.
    
    Before running this sample, you must set your Rambla user account credentials and the path to a local video file (to be encoded) in the settings below.
"""
USER = 'xxx' # add Rambla user account name
PWD = 'xxx' # add Rambla user account pwd
RASS_SERVER = "xxx" # either 'rass.cdn01.rambla.be' or 'rass.cdn02.rambla.be' (depending on the subCDN on which your account is located)
LOCAL_FILE = "/path/to/local/video/file" # add path to local video file, to be uploaded to the CDN

import sys, json, time
import raws_json
from raws_json.raws_service import RawsService, Feed, Query, RequestError
from raws_json.rass.service import RassService

try:
    # initialize client
    rass = RassService(username = USER, password = PWD, server = RASS_SERVER)

    # create a dir on the CDN
    dir = rass.createDir("crud_test/", True)
    print "Created dir with relative path = '%s'" % dir["entry"]["attrs"]["path"]

    # upload a file to a sub-directory (which will be created if it doesn't exist)
    item = rass.createItem("crud_test/subdir/", "filename.mp4", LOCAL_FILE)
    print "Created item with relative path = '%s' and size = %s" % (item["entry"]["attrs"]["path"], dir["entry"]["content"]["params"]["size"])
    
    # get list of all files in "crud_test/subdir/"
    print "Getting a list of all files in 'crud_test/subdir/' ..."
    feed = rass.getDirList(path = "crud_test/subdir/", query = Query(params = {"kind":"file"}))
    feed_obj = Feed(feed)
    for item in feed_obj.entries:
        print ".. found file with path = '%s', item instance url = %s" % (item["entry"]["attrs"]["path"], item["entry"]["id"])
        
    # check if file exists
    if rass.itemExists(item["entry"]["attrs"]["path"]):
        # delete file from CDN
        rass.deleteItem(item["entry"]["attrs"]["path"])

    # check if dir exists
    if rass.dirExists("crud_test/"):
        # delete dir from CDN (recursive)
        rass.deleteDir("crud_test/", True)

except RequestError, e:
    print "Error response returned by RAWS: %s" % unicode(e)

except Exception, e:
    print "Exception occurred: %s" % unicode(e)