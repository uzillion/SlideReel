import sys
import os
if os.path.exists('./dist'):
    sys.path.insert(0, 'dist/Lib/site-packages')
import twython
import webbrowser
import requests
import json
from twython import Twython
from requests_oauthlib import OAuth1
import re

class Twitter:
    def __init__(self):
        self.APP_TOKEN = 'aHuW9yrhN4ELuGSU5nYxvR6V3'
        self.APP_SECRET = 'yxsOWzPFjEENQ0qFM13tENpsTjfVUY13gwY7mv4HEXHvMElrZI'

    def authorize(self):
        req = Twython(self.APP_TOKEN, self.APP_SECRET)
        auth = req.get_authentication_tokens(callback_url='http://localhost:3000/twitter')
        REQUEST_TOKEN = auth['oauth_token']
        REQUEST_TOKEN_SECRET = auth['oauth_token_secret']
        webbrowser.open_new(auth['auth_url'])
        while True:
            try:
                open('oauth_cred.json', 'r')
                break;
            except:
                pass

        f=open('oauth_cred.json', 'r')
        obj = json.load(f)
        f.close()
        os.remove('./oauth_cred.json')
        OAUTH_VERIFIER = obj['oauth_verifier']
        twitter = Twython(self.APP_TOKEN, self.APP_SECRET, REQUEST_TOKEN, REQUEST_TOKEN_SECRET)
        tokens = twitter.get_authorized_tokens(OAUTH_VERIFIER)
        self.OAUTH_TOKEN = tokens['oauth_token']
        self.OAUTH_TOKEN_SECRET = tokens['oauth_token_secret']
        self.user_init()

    def user_init(self):
        self.twitter = Twython(self.APP_TOKEN, self.APP_SECRET, self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)

    def postImage(self, img):
        photo = open(img, 'rb')
        response = self.twitter.upload_media(media=photo)
        self.twitter.update_status(media_ids=[response['media_id']])

    def postVideo(self, vido):
        video = open('/path/to/file/video.mp4', 'rb')
        response = twitter.upload_video(media=video, media_type='video/mp4')
        self.twitter.update_status(status='Checkout this cool video!', media_ids=[response['media_id']])

## Uncomment the following lines to test script:
# tweet = Twitter()
# tweet.authorize()
# tweet.postImage('./WR2.jpg')
