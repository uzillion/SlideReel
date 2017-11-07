'''
Date modified: 11/06/2017

This module makes use of sharing APIs accross different social media sites.

BASIC USAGE:
1) Create instance of social media class. Eg:- twitter = Twitter()
2) Get authorization from the user. Eg:- <social media instance>.authorize()
3) Post image/video. Eg:- <social media instance>.postImage(<image path>)
'''

import sys
import os
# if os.path.exists(os.getcwd()+'./dependencies'):
sys.path.insert(0, './social/dependencies/Lib/site-packages')
import twython
import re
import webbrowser
import requests
import json
import time
import facebook
from twython import Twython
from selenium import webdriver
from requests_oauthlib import OAuth1

try:
    os.remove('./social/oauth_cred.json')
except:
    pass


# ============================= Twitter ===============================
class Twitter:
    def __init__(self):
        self.APP_TOKEN = 'aHuW9yrhN4ELuGSU5nYxvR6V3'
        self.APP_SECRET = 'yxsOWzPFjEENQ0qFM13tENpsTjfVUY13gwY7mv4HEXHvMElrZI'
        self.MEDIA_UPLOAD_URL = 'https://upload.twitter.com/1.1/media/upload.json'
        self.MEDIA_POST_URL = 'https://api.twitter.com/1.1/statuses/update.json'

    def authorize(self):
        req = Twython(self.APP_TOKEN, self.APP_SECRET)
        auth = req.get_authentication_tokens(callback_url='http://localhost:3000/twitter')
        REQUEST_TOKEN = auth['oauth_token']
        REQUEST_TOKEN_SECRET = auth['oauth_token_secret']
        webbrowser.open_new(auth['auth_url'])

        # Makes program wait till OAuth credentials are ready to be read
        while True:
            try:
                open('./social/oauth_cred.json', 'r')
                break;
            except:
                pass

        # Prevents reading the file before server finishes to write it.
        time.sleep(1)

        # Loads OAuth data from JSON file
        f=open('./social/oauth_cred.json', 'r')
        obj = json.load(f)
        f.close()
        # Removing to prevent future access
        os.remove('./social/oauth_cred.json')

        OAUTH_VERIFIER = obj['oauth_verifier']
        twitter = Twython(self.APP_TOKEN, self.APP_SECRET, REQUEST_TOKEN, REQUEST_TOKEN_SECRET)

        # Gets Access tokens from twitter
        tokens = twitter.get_authorized_tokens(OAUTH_VERIFIER)

        # Stores Access Tokens in respective variables
        self.OAUTH_TOKEN = tokens['oauth_token']
        self.OAUTH_TOKEN_SECRET = tokens['oauth_token_secret']
        self.SCREEN_NAME = tokens['screen_name']
        self.user_init()

    # Creates twitter app user
    def user_init(self):
        self.oauth = OAuth1(self.APP_TOKEN, self.APP_SECRET, self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)
        self.twitter = Twython(self.APP_TOKEN, self.APP_SECRET, self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)

    def postImage(self, img):
        photo = open(img, 'rb')
        response = self.twitter.upload_media(media=photo)
        self.twitter.update_status(media_ids=[response['media_id']])
        webbrowser.open_new("http://localhost:3000/twitter?status=completed&name="+self.SCREEN_NAME)


    def postVideo(self, video):
        self.video = video
        self.video_size = os.path.getsize(video)
        self.videoInit()
        self.videoAppend()
        self.videoFinalize()
        data = {
          'media_ids': self.media_id
        }

        req = requests.post(url=self.MEDIA_POST_URL, data=data, auth=self.oauth)
        # print(req.json())

        # TWYTHON EXPERIMENTAL CODE:
        # video = open(video, 'rb')
        # response = self.twitter.upload_video(media=video, media_type='video/mp4')
        # self.twitter.update_status(status='Checkout this cool video!', media_ids=[response['media_id']])

    def videoInit(self):
        data = {
          'command': 'INIT',
          'media_type': 'video/mp4',
          'total_bytes': self.video_size,
          'media_category': 'tweet_video'
        }

        req = requests.post(url=self.MEDIA_UPLOAD_URL, data=data, auth=self.oauth)
        self.media_id = req.json()['media_id']
        # print('Media ID: %s' % str(self.media_id))

    def videoAppend(self):
        segment_id = 0
        bytes_sent = 0
        file = open(self.video, 'rb')

        while bytes_sent < self.video_size:
            chunk = file.read(4*1024*1024)
            print('Sending segment {}'.format(segment_id+1))

            data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id
            }

            files = {
                'media':chunk
            }

            req = requests.post(url=self.MEDIA_UPLOAD_URL, data=data, files=files, auth=self.oauth)

            if req.status_code < 200 or req.status_code > 299:
                print(req.status_code)
                print(req.text)
                sys.exit(0)

            segment_id = segment_id + 1
            bytes_sent = file.tell()

            print('{} of {} bytes uploaded'.format(str(bytes_sent), str(self.video_size)))

        print('Upload chunks complete.')

    def videoFinalize(self):
        print('FINALIZE')

        data = {
          'command': 'FINALIZE',
          'media_id': self.media_id
        }

        req = requests.post(url=self.MEDIA_UPLOAD_URL, data=data, auth=self.oauth)
        # print(req.json())

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()

    def check_status(self):
        if self.processing_info is None:
            return

        state = self.processing_info['state']

        print('Media processing status is %s ' % state)

        if state == u'succeeded':
            webbrowser.open_new("http://localhost:3000/twitter?status=completed&name="+self.SCREEN_NAME)
            return

        if state == u'failed':
            print("Upload Failed")
            sys.exit(0)

        check_after_secs = self.processing_info['check_after_secs']

        print('Checking after {} seconds'.format(str(check_after_secs)))
        time.sleep(check_after_secs)

        print('STATUS')

        params = {
          'command': 'STATUS',
          'media_id': self.media_id
        }

        req = requests.get(url=self.MEDIA_UPLOAD_URL, params=params, auth=self.oauth)

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()


# ============================ Facebook ===============================
class Facebook:
    def __init__(self):
        self.__ACCESS_TOKEN = ""
        self.__USER_ID = ""


    def authorize(self):
        # Starts the facebook authorization script on the server
        driver = webdriver.Chrome()
        driver.get("http://localhost:3000/facebook")

        # Makes program wait till OAuth credentials are ready to be read
        while True:
            try:
                open('oauth_cred.json', 'r')
                break;
            except:
                pass

        # Prevents reading the file before server finishes to write it.
        time.sleep(1)

        # Loads OAuth data from JSON file
        f=open('./social/oauth_cred.json', 'rb')
        obj = json.load(f)
        f.close()
        # Removing to prevent future access
        os.remove('./social/oauth_cred.json')

        # Stores Access Tokens in respective variables
        self.__ACCESS_TOKEN = obj['ACCESS_TOKEN']
        self.__USER_ID = obj['USER_ID']
        self.graph = facebook.GraphAPI(access_token=self.__ACCESS_TOKEN, version="2.1")

    def postImage(self, img):
        self.graph.put_photo(image=open(img, 'rb'),
                album_path=self.__USER_ID + "/photos")

    def postVideo(self, video):
        self.graph.put_video(video=open(video, 'rb'),
                album_path=self.__USER_ID + "/videos")
