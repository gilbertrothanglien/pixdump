# Distinctiveness and Complexity

### This is my final project for cs50w. This project is distinct from other projects we did on the course as it is an image hosting site.

### This project satisfies the requirements as it is distinct from others and uses java script and Django. In this project, image can be uploaded either as public or private image and is mobile responsive. When uploading image on private it will not show up on the home page, category page and profile page. Only people with the link will be able to view the image. Other users will be able to view, like and download images. Users who are signed in will be able to follow other users so that the public post made by the followed user will be visible on the following page of the user. Users who are signed in will be able to edit their profile page by uploading profile picture, First name, last name, occupation and bio.


## What’s contained in each file

### imagesite app is the main app for the project
	* The templates folder contains all the templates rendered by the application
	* index.html is for the home page, category.html for image categories and so on
	* The uploaded pictures are stored in static/images/uploads
	* The profile picture uploaded is stored in static/images/profile_images
	* The static folder contains all the static files like css, js and images.
	* Java Script files in static/js directory
	* Css files in static/css directory

### Templates folder contains all the templates for each page. 
	* layout.html is the layout of most of the pages
	* index.html for home page
	* category.html for the categories of images the user request
	* edit_profile.html for the authenticated user to edit their profile.
	* following.html for users to see the post of their followed users.
	* user_profile.html to display profile of users
	* view_image.html to display a specific image and make user able to download the image
	* upload_image.html is page for uploading images
	* error.html to display any request error by the user

### Static files
	* All the static files like css and js helps the UI looks better and make it more dynamic
	* Each of the html file have their own css with the same name but extension changed from html to css or js.

### .py files
	* views.py file contains all the view function. It handles all the request like login, register, edit profile, upload_image, etc given by the users.
	* urls.py file contains all the path of the request that can be made by the user and according to the path requested, it calls the respective functions from the views.py
	* models.py contains all my models of the database.



# How to run the application
	* As I dont use any external module other than django there are no other requirements
	* Go into the main directory with terminal or cmd and start the project. "python manage.py runserver"

### Since i don't use any external packages other than django, I don't include requirements.txt file.