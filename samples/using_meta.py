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

""" This sample demonstrates how to use the META service to produce metadata content and do searches.
    
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
    # upload some files to the the 'meta_sample' dir on the CDN (so we can attach metadata to them)
    item1 = rass.createItem("meta_sample/", "elephants_dream.mp4", LOCAL_FILE)
    item1b = rass.createItem("meta_sample/", "elephants_dream.jpg", LOCAL_FILE)
    print "Created item instances : %s + %s " % (item1["entry"]["id"], item1b["entry"]["id"])
    item2 = rass.createItem("meta_sample/", "big_buck_bunny.mp4", LOCAL_FILE)
    print "Created item instance : %s " % item2["entry"]["id"]
    item3 = rass.createItem("meta_sample/", "sintel.mp4", LOCAL_FILE)
    print "Created item instance : %s " % item3["entry"]["id"]
    item4 = rass.createItem("meta_sample/", "yo_frankie.mp4", LOCAL_FILE) # we will not attach metadata to this item
    print "Created item instance : %s " % item4["entry"]["id"]

    # create vocabs
    if not meta.vocabExists(name = "media"):
        vocab_obj = Vocab(name = "media", description = "Media RSS", xml_namespace = "http://search.yahoo.com/mrss/")
        vocab = meta.createVocab(vocab_obj.to_entry())
        print "Created vocab instance : %s " % vocab["entry"]["id"]
    if not meta.vocabExists(name = "myvocab"):
        vocab_obj = Vocab(name = "myvocab", description = "My custom vocab", xml_namespace = "http://myvocab.org/ns/")
        vocab2 = meta.createVocab(vocab_obj.to_entry())
        print "Created vocab instance : %s " % vocab2["entry"]["id"]

    # Create content instance for "meta_sample/elephants_dream.mp4" + "meta_sample/elephants_dream.jpg"
    print "Adding metadata for video file = '%s' ..." % item1["entry"]["attrs"]["path"]
    content_obj = MetaContent(name = "elephants_dream")
    content_obj.add_file_objs([FileObj(path = item1["entry"]["attrs"]["path"]), FileObj(path = item1b["entry"]["attrs"]["path"])])
    content_obj.add_meta_obj(meta_name = "title", vocab = "media", text = "Elephants Dream")
    content_obj.add_meta_obj(meta_name = "description", vocab = "media", text = "Elephants Dream is a computer-generated short film that was produced almost completely using the free software 3D suite Blender")
    content_obj.add_meta_obj(meta_name = "keywords", vocab = "media", text = "elephant, animation, Blender")
    content_obj.add_meta_obj(meta_name = "credit", vocab = "media", text = "Blender Foundation", attrs = {"role":"author",})
    content_obj.add_meta_obj(meta_name = "link", vocab = "rss", attrs = {"href":"http://mysite.org/elephants_dream",})
    content1 = meta.createContent(content_obj.to_entry())
    print ".. created content instance : %s " % content1["entry"]["id"]

    # Create content instance with multiple languages for "meta_sample/big_buck_bunny.mp4"
    print "Adding metadata for video file = '%s'" % item2["entry"]["attrs"]["path"]
    content_obj = MetaContent(name = "big_buck_bunny")
    content_obj.add_file_obj(FileObj(path = item2["entry"]["attrs"]["path"]))
    content_obj.add_meta_obj(meta_name = "title", vocab = "media", text = "Big Buck Bunny", lang = "en")
    content_obj.add_meta_obj(meta_name = "description", vocab = "media", text = "Big Buck Bunny is a short computer animated film by the Blender Institute, part of the Blender Foundation.", lang = "en")
    content_obj.add_meta_obj(meta_name = "keywords", vocab = "media", text = "bunny, animation, Blender", lang = "en")
    content_obj.add_meta_obj(meta_name = "title", vocab = "media", text = "Big Buck Bunny", lang = "nl")
    content_obj.add_meta_obj(meta_name = "description", vocab = "media", text = "Big Buck Bunny is een animatiefilm gemaakt door het Blender Institute met behulp van opensource software.", lang = "nl")
    content_obj.add_meta_obj(meta_name = "keywords", vocab = "media", text = "konijn, animatie, Blender", lang = "nl")
    content_obj.add_meta_obj(meta_name = "tag", vocab = "myvocab", text = "animation", lang = "en")
    content_obj.add_meta_obj(meta_name = "tag", vocab = "myvocab", text = "animatie", lang = "nl")
    content_obj.add_meta_obj(meta_name = "tag", vocab = "myvocab", text = "animation", lang = "fr")
    content2 = meta.createContent(content_obj.to_entry())
    print ".. created content instance : %s " % content2["entry"]["id"]

    # Create content instance without meta objects for "meta_sample/sintel.mp4"
    print "Creating content object without meta objects for video file = '%s'" % item3["entry"]["attrs"]["path"]
    content_obj = MetaContent(name = "sintel")
    content_obj.add_file_obj(FileObj(path = item3["entry"]["attrs"]["path"]))
    content3 = meta.createContent(content_obj.to_entry())
    print ".. created content instance : %s " % content3["entry"]["id"]

    # Update content instance, adding meta objects
    print "Updating content object with meta objects for video file = '%s'" % item3["entry"]["attrs"]["path"]
    content_obj = MetaContent(entry = content3)
    content_obj.add_meta_obj(meta_name = "title", vocab = "media", text = "Sintel")
    content_obj.add_meta_obj(meta_name = "summary", vocab = "media", text = "Sintel (code-named Durian) is a short computer animated film by the Blender Institute, part of the Blender Foundation.", lang = "en")
    content_obj.add_meta_obj(meta_name = "tag", vocab = "myvocab", text = "animation", lang = "en")
    content3 = meta.updateContent(content_obj.to_entry())
    print ".. updated content instance : %s " % content3["entry"]["id"]

    # Get all content from the 'meta_sample/' dir (including files without a content instance)
    print "Getting contentdir list for 'meta_sample/' ..."
    feed = meta.getContentDirList(dirpath = "meta_sample/")
    feed_obj = Feed(feed)
    for content in feed_obj.entries:
        print ".. found content instance with name = '%s' and %d file(s). Meta objects:" % (content["entry"]["content"]["params"]["name"], len(content["entry"]["content"]["file"]))
  
    # Get feed 
    print "Getting content list, using meta=myvocab:tag:animation + lang=en ..."
    feed = meta.getContentList(query = Query(params = {"meta":"myvocab:tag:animation", "lang":"en"}))
    feed_obj = Feed(feed)
    for content in feed_obj.entries:
        print ".. found content instance with name = '%s' and %d file(s)" % (content["entry"]["content"]["params"]["name"], len(content["entry"]["content"]["file"]))
        content_obj = MetaContent(entry = content)
        for meta_obj in content_obj.get_meta_objs():
            print "   * %s" % unicode(meta_obj)

    # Get feed 
    print "Getting content list, using iqmeta=blender ..."
    feed = meta.getContentList(query = Query(params = {"iqmeta":"blender"}))
    feed_obj = Feed(feed)
    for content in feed_obj.entries:
        print ".. found content instance with name = '%s' and %d file(s)" % (content["entry"]["content"]["params"]["name"], len(content["entry"]["content"]["file"]))
        content_obj = MetaContent(entry = content)
        for meta_obj in content_obj.get_meta_objs():
            print "   * %s" % unicode(meta_obj)

    # Delete the content instances
    meta.deleteContent(content1)
    meta.deleteContent(content2)
    meta.deleteContent(content3)
    print "Deleted content + files."

    # delete the files on the CDN
    if rass.dirExists("meta_sample/"):
        rass.deleteDir("meta_sample/", True)
        print "Deleted 'meta_sample' dir from CDN."


except RequestError, e:
    print "Error response returned by RAWS: %s" % unicode(e)

except Exception, e:
    print "Exception occurred: %s" % unicode(e)