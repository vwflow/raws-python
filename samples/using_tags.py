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

""" This sample demonstrates how to use the META service to work with tags.
    
    Before running this sample, you must set your Rambla user account credentials and the path to a local video file (to be encoded) in the settings below.

    Warning: this sample will remove a 'meta_sample' directory if it exists within your CDN account !
"""
USER = 'xxx' # add Rambla user account name
PWD = 'xxx' # add Rambla user account pwd
RASS_SERVER = "xxx" # either 'rass.cdn01.rambla.be' or 'rass.cdn02.rambla.be' (depending on the subCDN on which your account is located)
LOCAL_FILE = "/path/to/local/video/file" # add path to local video file, to be uploaded to the CDN

import sys, json, time
import raws_json
from raws_json.raws_service import RawsService, Feed, Query, RequestError
from raws_json.meta.meta import *
from raws_json.meta.vocab import Vocab
from raws_json.rass.service import RassService
from raws_json.meta.service import MetaService

# initialize client
rass = RassService(username = USER, password = PWD, server = RASS_SERVER)
meta = MetaService(username = USER, password = PWD)

try:
    # upload some files to the the 'meta_sample' dir on the CDN  (so we can attach metadata to them)
    item1 = rass.createItem("meta_sample/", "elephants_dream.mp4", LOCAL_FILE)
    item1b = rass.createItem("meta_sample/", "elephants_dream.jpg", LOCAL_FILE)
    print "Created item instances : %s + %s " % (item1["entry"]["id"], item1b["entry"]["id"])
    item2 = rass.createItem("meta_sample/", "big_buck_bunny.mp4", LOCAL_FILE)
    print "Created item instance : %s " % item2["entry"]["id"]
    item3 = rass.createItem("meta_sample/", "sintel.mp4", LOCAL_FILE)
    print "Created item instance : %s " % item3["entry"]["id"]

    # Create content instance for "meta_sample/elephants_dream.mp4" + "meta_sample/elephants_dream.jpg"
    print "Adding metadata for video file = '%s' ..." % item1["entry"]["content"]["params"]["path"]
    content_obj = MetaContent(name = "elephants_dream")
    content_obj.add_file_objs([FileObj(path = item1["entry"]["content"]["params"]["path"]), FileObj(path = item1b["entry"]["content"]["params"]["path"])])
    content_obj.add_tags(["Blender", "elephant", "animation"])
    content1 = meta.createContent(content_obj.to_entry())
    print ".. created content instance : %s " % content1["entry"]["id"]

    # Create content instance with multiple languages for "meta_sample/big_buck_bunny.mp4"
    print "Adding metadata for video file = '%s'" % item2["entry"]["content"]["params"]["path"]
    content_obj = MetaContent(name = "big_buck_bunny")
    content_obj.add_file_obj(FileObj(path = item2["entry"]["content"]["params"]["path"]))
    content_obj.add_tags(["Blender", "bunny", "animation"])
    content2 = meta.createContent(content_obj.to_entry())
    print ".. created content instance : %s " % content2["entry"]["id"]

    # Create content instance without meta objects for "meta_sample/sintel.mp4"
    print "Creating content object without meta objects for video file = '%s'" % item3["entry"]["content"]["params"]["path"]
    content_obj = MetaContent(name = "sintel")
    content_obj.add_file_obj(FileObj(path = item3["entry"]["content"]["params"]["path"]))
    content_obj.add_tag("Blender")
    content3 = meta.createContent(content_obj.to_entry())
    print ".. created content instance : %s " % content3["entry"]["id"]

    # Update content instance, adding meta objects
    print "Updating content object with meta objects for video file = '%s'" % item3["entry"]["content"]["params"]["path"]
    content_obj = MetaContent(entry = content3)
    content_obj.add_tags(["sintel", "animation"])
    content3 = meta.updateContent(content_obj.to_entry())
    print ".. updated content instance : %s " % content3["entry"]["id"]

    # Get all content from the 'meta_sample/' dir (including files without a content instance)
    print "Getting contentdir list for 'meta_sample/' ..."
    feed = meta.getContentDirList(dirpath = "meta_sample/")
    feed_obj = Feed(feed)
    for content in feed_obj.entries:
        content_obj = MetaContent(entry = content)
        print ".. found content instance with name = '%s' and %d file(s). Tags = %s." % (content["entry"]["content"]["params"]["name"], len(content["entry"]["content"]["file"]), unicode(content_obj.get_tags()))
  
    # Get feed 
    print "Getting content list, using tag=Blender ..."
    feed = meta.getContentList(query = Query(params = {"tag":"Blender"}))
    feed_obj = Feed(feed)
    for content in feed_obj.entries:
        content_obj = MetaContent(entry = content)
        print ".. found content instance with name = '%s' and %d file(s). Tags = %s." % (content["entry"]["content"]["params"]["name"], len(content["entry"]["content"]["file"]), unicode(content_obj.get_tags()))

    # Get feed 
    print "Getting content list, using iqtag=Eleph,Bunny ..."
    feed = meta.getContentList(query = Query(params = {"iqtag":"Eleph,Bunny"}))
    feed_obj = Feed(feed)
    for content in feed_obj.entries:
        content_obj = MetaContent(entry = content)
        print ".. found content instance with name = '%s' and %d file(s). Tags = %s." % (content["entry"]["content"]["params"]["name"], len(content["entry"]["content"]["file"]), unicode(content_obj.get_tags()))

    # Delete the content instances
    meta.deleteContent(content1)
    meta.deleteContent(content2)
    meta.deleteContent(content3)
    print "Deleted content + files."

    # delete the files on the CDN
    if rass.dirExists("meta_sample/"):
        rass.deleteDir("meta_sample/")
        print "Deleted 'meta_sample' dir from CDN."

except RequestError, e:
    print "Error response returned by RAWS: %s" % unicode(e)

except Exception, e:
    print "Exception occurred: %s" % unicode(e)