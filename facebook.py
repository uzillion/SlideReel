import sys
import os
if os.path.exists('./dist'):
    sys.path.insert(0, 'dist/Lib/site-packages')
import json
from selenium import webdriver
import time
import facebook

class Facebook:
    def __init__(self):
        self.ACCESS_TOKEN = ""
        self.USER_ID = ""


    def authorize(self):
        driver = webdriver.Chrome()
        driver.get("http://localhost:3000/facebook")
        while True:
            try:
                open('oauth_cred.json', 'r')
                break;
            except:
                pass

        time.sleep(1)
        f=open('oauth_cred.json', 'rb')
        obj = json.load(f)
        f.close()
        os.remove('./oauth_cred.json')
        self.ACCESS_TOKEN = obj['ACCESS_TOKEN']
        self.USER_ID = obj['USER_ID']
        self.graph = facebook.GraphAPI(access_token=self.ACCESS_TOKEN, version="2.1")

    def postImage(self, img):
        self.graph.put_photo(image=open(img, 'rb'),
                album_path=self.USER_ID + "/photos")

    def postVideo(self, video):
        self.graph.put_video(video=open(video, 'rb'),
                album_path=self.USER_ID + "/videos")

## Uncomment the following lines to test script:
fb = Facebook()
fb.authorize()
# fb.postImage("WR2.jpg")
# fb.postVideo("SampleVideo_360x240_1mb.mp4")
