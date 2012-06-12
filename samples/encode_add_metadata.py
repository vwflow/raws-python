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

""" This sample demonstrates how to encode a media file, add metadata to it and retrieve playlists based on the metadata. 

    If you have YouTube syncing enabled (default = disabled), the media file will also be uploaded to YouTube and the metadata will be synced.
    Warning: when the metadata are synced, the YouTube video will become publicly available.
    
    Note: to run this sample, you must have metadata support + YouTube syncing turned on for your user account (contact support@rambla.be for more info).
    Before running this sample, you must set your Rambla user account credentials and the path to a local video file (to be encoded) in the settings below.
"""
USER = 'xxx' # add Rambla user account name
PWD = 'xxx;;' # add Rambla user account pwd
LOCAL_FILE = "/path/to/local/video/file" # add path to local video file, to be encoded and published by RAWS

import sys, json, time
import raws_json
from raws_json.raws_service import RawsService, Feed, Query, RequestError
from raws_json.meta.meta import *
from raws_json.rats.service import RatsService
from raws_json.meta.service import MetaService

try:
    # initialize clients
    rats = RatsService(username = USER, password = PWD)
    meta = MetaService(username = USER, password = PWD)

    # PART 1 : ENCODE VIDEO FILE
    # --------------------------

    # upload a src video for encoding 
    print "Uploading src, please wait..."
    src = rats.createSrc(filename = "myvideo", local_path = LOCAL_FILE)
    
    # encode your video to mp4 (for online viewing) with same dimensions + make snapshots (formatgroup = 1)
    print "Launching encoding job..."
    job = rats.createJob(formatgroup = rats.ENCODE_MP4_480P_WITH_SNAPSHOTS, # encode your video to mp4 (480p, for online viewing) + make snapshots
                         snapshot_interval = "50", # make 3 snapshot (one at the start of your video, one at 50%, and one at the end (100%))
                         output = rats.EXPORT_TO_CDN, # publish transcoded files on the CDN
                         src_location = src["entry"]["content"]["params"]["filename"], # use the src we've just uploaded
                         tgt_location = "test/big_buck_bunny", # publish the encoded file as big_buck_bunny (the right extension will be added automatically) in the test directory on the CDN
                         proc = "%s,%s" % (rats.MAIL_CDN_REPORT, rats.MAIL_HUMAN_READABLE)) # send emails with the results
    while int(job["entry"]["content"]["params"]["batch_status"]) < 100:
        time.sleep(10)
        print ".. batch status = %s for job %s, polling..." % (job["entry"]["content"]["params"]["batch_status"], job["entry"]["id"])
        job = rats.getJob(uri = job["entry"]["id"])
    
    # check if job has succeeded    
    if int(job["entry"]["content"]["params"]["status"]) != rats.JOB_SUCCEEDED:
        print "Job %s failed with status = %s" % (job["entry"]["id"], job["entry"]["content"]["params"]["status"])
        sys.exit(int(job["entry"]["content"]["params"]["status"]))


    # PART 2 : ADD METADATA
    # ---------------------
    
    # if succeeded, the job entry will also contains the CDN report
    # RATS has created a META content instance for our encoded files => get the URL for the content instance from this CDN report
    print "Retrieving META content instance at %s .." % job["entry"]["cdn_report"]["content"]
    
    # retrieve the new content entry (if YouTube export is enabled, the content entry will also contain the ID of a private YouTube video)
    content = meta.getContent(job["entry"]["cdn_report"]["content"])
    print "Retrieved content instance with name = %s and YouTube ID = %s" % (content["entry"]["content"]["params"]["name"], content["entry"]["content"]["params"]["yt_id"])
    
    # transfer content entry into object + update it
    content_obj = MetaContent(entry = content)
    
    content_obj.add_meta_obj(meta_name = "title", vocab = "media", text = "Big Buck Bunny", lang = "en")
    content_obj.add_meta_obj(meta_name = "description", vocab = "media", text = "Big Buck Bunny is a short computer animated film by the Blender Institute, part of the Blender Foundation.", lang = "en")
    content_obj.add_meta_obj(meta_name = "keywords", vocab = "media", text = "bunny, animation, Blender", lang = "en")
    
    content_obj.add_meta_obj(meta_name = "title", vocab = "media", text = "Big Buck Bunny", lang = "nl")
    content_obj.add_meta_obj(meta_name = "description", vocab = "media", text = "Big Buck Bunny is een animatiefilm gemaakt door het Blender Institute met behulp van opensource software.", lang = "nl")
    content_obj.add_meta_obj(meta_name = "keywords", vocab = "media", text = "konijn, animatie, Blender", lang = "nl")
    
    content_obj.add_meta_obj(meta_name = "title", vocab = "media", text = "Big Buck Bunny", lang = "fr")
    content_obj.add_meta_obj(meta_name = "description", vocab = "media", text = "Big Buck Bunny s'inscrit dans la lignée directe du court-métrage Elephants Dream, produit en 2005-2006.", lang = "fr")
    content_obj.add_meta_obj(meta_name = "keywords", vocab = "media", text = "lapin, animation, Blender", lang = "fr")
    
    # send updated entry to META, adding sync_yt=1 in querystring (=> metadata will be synced to YouTube + yt video will become public)
    content = meta.updateContent(entry = content_obj.to_entry(), query = Query(params = {"sync_yt":"1"}))
    print "Updated content instance, YouTube video made public."

    # print some info about this content instance
    content_obj = MetaContent(entry = content)
    print "Meta objects for content instance with name = %s" % content_obj.name
    for m in content_obj.get_meta_objs():
        print ".. %s:%s with text = %s (lang=%s) and attributes = %s" % (m.vocab, m.meta_name, m.text, m.lang, unicode(m.attrs))
    print "Files linked to content instance with name = %s" % content_obj.name
    for f in content_obj.get_file_objs():
        print ".. %s file with path = %s, width = %s, height = %s, duration = %s" % (f.media_type, f.path, f.width, f.height, f.duration)


    # PART 3 : RETRIEVE FEEDS / PLAYLISTS
    # -----------------------------------

    # retrieve external atom feed, using case insensitive search for the keyword Lapin (lang=fr)
    feed = meta.getExtAtom(query = Query(params = {"iqmeta":"Lapin", "lang":"fr"}))
    print "Atom feed retrieved as a result of (case insensitive) keyword search:"
    print unicode(feed)
    print feed

    # retrieve media rss playlist, using (case sensitive) search on the title
    feed = meta.getExtMrss(query = Query(params = {"meta":"media:title:Big Buck Bunny"}))
    print "Media RSS feed retrieved as a result of a qualified search:"
    print unicode(feed)
    
    # retrieve the same media rss playlist, but with streaming video (via rtmp)
    feed = meta.getExtMrss(rtmp = True, query = Query(params = {"meta":"media:title:Big Buck Bunny"}))
    print "Media RSS feed retrieved as a result of a qualified search:"
    print unicode(feed)
    
    # CLEANUP
    # -------
    # delete META content + encoded files from the CDN
    meta.deleteContent(content)     
    print "Deleted META content + files from CDN."

except RequestError, e:
    print "Error response returned by RAWS: %s" % unicode(e)

except Exception, e:
    print "Exception occurred: %s" % unicode(e)