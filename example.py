from social.share import *

# twitter = Twitter()
# twitter.authorize()
# twitter.postVideo("./sample_video.mp4")
# twitter.postImage("./sample_image.jpg")

facebook = Facebook()
facebook.authorize()
# facebook.postImage("./sample_image.jpg")
facebook.postVideo("./sample_video.mp4")
