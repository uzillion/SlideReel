# Social
### Usage
1. In your terminal, in the social directory, type: `$ npm install`<br><br>
2. Run the node server through your terminal by using the "share.js" file.<br><br>
3. Import this library in your program by typing:<br>
   ```python
   from social.share import *
   ```
4. Instantiate the social media class name. Eg:- `twitter = Twitter()`<br><br>
5. Authorize the app by accessing the "authorize()" method in social media class. Eg:-
   ```
   facebook = Facebook()
   facebook.authorize()
   ```
6. Use "&lt;social media instance&gt;.postImage(&lt;image path&gt;)" to post images<br><br>
7. Use "&lt;social media instance&gt;.postImage(&lt;video path&gt;)" to post videos
