## User notes
The given software offers a platform for studies discussion board and planning events.  <br>
Users can choose to browse the website without signing up, however some features are limited for non-registered users. <br>
During the sign-up process, the user would be prompted to verify their email address through a one-time password and later will have to choose an appropriate password. <br>
After signing up, the user can log in to access additional features. Aside from simply browsing the homepage, a registered user can: -
1. Upload posts
2. Comment under any post
3. Add events
4. Manage event participants
5. Add user profile information
The user may choose to delete their posts and may even choose
to completely delete their profile and all associated items with
it.
## Developer notes
### Installation
To run the software, first install the following libraries in your python environment –
1. Django
2. Pillow
3. Widget_tweaks <br>
After installing all the necessary libraries, go inside the project directory and run python manage.py runserver <br>
The app should start without any issues.
Features
The software includes the functionalities of –
- Browsing
- Downloading files
- Uploading posts
- Adding multimedia items
- Commenting
- Creating events
- Managing event participants
- Adding profile information <br>
Some features are still under development . <br>
### Bugs and Issues <br>
1. The software has a comparatively high response time while
sending any mail to the user.
- Potential fix is changing the mail backend
2. Currently, the data is being stored locally and can be
shifted onto a cloud server when the app is deployed in
production.
- More information regarding the user’s interests can be
stored to display posts that are better suited to the user’s
tastes.
