# Social
### Usage
<li>In your terminal, in the social directory, type:
```
$ npm install``` 
<li>Run the node server through your terminal by using the "share.js" file.
<li>Import this library in your program by typing:<br>
```python
from social.share import *
```
<li>Instantiate the social media class name. Eg:-
```
twitter = Twitter()```
<li>Authorize the app by accessing the "authorize()" method in social media class. Eg:-
```
facebook = Facebook()
facebook.authorize()```
<li>Use "&lt;social media instance&gt;.postImage(&lt;image path&gt;)" to post images
<li>Use "&lt;social media instance&gt;.postImage(&lt;video path&gt;)" to post videos
