import sys
import os
if os.path.exists('/dist'):
    sys.path.insert(0, 'dist/Lib/site-packages')
import twython
import webbrowser
import requests
import json
from twython import Twython
from requests_oauthlib import OAuth1
import re

class share:
    def __init__(self):
        self.APP_TOKEN = 'aHuW9yrhN4ELuGSU5nYxvR6V3'
        self.APP_SECRET = 'yxsOWzPFjEENQ0qFM13tENpsTjfVUY13gwY7mv4HEXHvMElrZI'


    def authorize(self):
        url = 'https://api.twitter.com/oauth/request_token'
        auth = OAuth1(self.APP_TOKEN, self.APP_SECRET)
        r=requests.post(url, auth=auth)
        temp = re.search('oauth_token=(.+?)&', r.text)
        REQUEST_TOKEN=temp.group(1)
        request_url = 'https://api.twitter.com/oauth/authorize?oauth_token='+REQUEST_TOKEN

        # Open webview and prompt authorization.
        # On authorization load oauth_token and oauth_verifier
        # Eg:- webbrowser.open_new(request_url)

        # Assuming authorized:
        r=requests.post('https://api.twitter.com/oauth/access_token?oauth_verifier='+OAUTH_VERIFIER)
        temp = re.search('oauth_token=(.+?)&', r.text)
        self.OAUTH_TOKEN = temp.group(1)
        temp = re.search('oauth_token_secret=(.+?)&', r.text)
        self.OAUTH_TOKEN_SECRET = temp.group(1)
        temp = re.search('user_id=(.+?)&', r.text)
        self.USER_ID = temp.group(1)
        self.user_init()

    def user_init(self):
        self.twitter = Twython(self.APP_TOKEN, self.APP_SECRET, self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)

    def postImage(self, img):
        photo = open(img, 'rb')
        response = twitter.upload_media(media=photo)
        self.twitter.update_status(media_ids=[response['media_id']])

    def postVideo(self, vido):
        video = open('/path/to/file/video.mp4', 'rb')
        response = twitter.upload_video(media=video, media_type='video/mp4')
        self.twitter.update_status(status='Checkout this cool video!', media_ids=[response['media_id']])

# Untag the following line to test script:
# reqCreden()
