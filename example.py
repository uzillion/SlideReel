from social.share import *

twitter = Twitter()
print(twitter.APP_TOKEN)
twitter.authorize()
twitter.postVideo("./sample_video.mp4")
# twitter.postImage("./sample_image.jpg")
