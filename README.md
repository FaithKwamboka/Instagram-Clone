## Author
> Faith Kwamboka Okong'o

# Kwash Gram
This is an app that allows users to post pics, get followers, follow other users, like and comment on posts.

![gram](https://user-images.githubusercontent.com/100117264/172257832-e9e80537-8119-4914-adb1-69bea4361737.png)


## User Stories
As a user of the application I should be able to:
* Sign in to the application to start using.
* Upload my pictures to the application.
* See my profile with all my pictures.
* Follow other users and see their pictures on my timeline.
* Like a picture and leave a comment on it.

## Specifications
| Behaviour | Input | Output |
| :---------------- | :---------------: | ------------------: |
| Admin Authentication | **On demand** | Access Admin dashboard |
| User Authentication | **On demand, verify emails before proceeding** | Access Admin dashboard |
| Display all images with comments and likes | **Home page** | Clickable links to open any images in a modal |
| Display single images on modal | **On  click** | All details should be viewed|
| To add an image  | **Through Admin dashboard and homepage** | Click on add and upload respectively|
| To edit image  | **Through Admin dashboard** | Redirected to the  image form details and editing happens|
| To delete an image  | **Through Admin dashboard** | click on image object and confirm by delete button|
| To search  | **Enter text in search bar** | Users can search by username|
| View other users profiles via story menu bar | **Click username on user stories navigation** | Users can view all images posted by any user|
| Comment on images | **Add comments below respective image** | Users can add comments on any image|
| Like images | **Add likes to an image** | Users can add likes to images they like|

## Technologies used
* Python3
* Django & postresql
* Html5
* Css3
* Bootstrap4


## Installations

The following command installs all the application requirements
>``pip freeze -r requirements.txt``

## Setup
Run 
``https://github.com/FaithKwamboka/Instagram-Clone.git``

or download the zip file from github.

After extracting the files, 

1. Navigate to the project folder
>`` cd name_of_folder`` 

2. Creating a virtual environment
>``virtualenv virtual``

3. Activating the virtual environment
>``source virtual/bin/activate``

4. Running the application
>``python3 manage.py runserverserver``

5. Running tests

 > ``python3 manage.py test.``

## [License](https://github.com/FaithKwamboka/Instagram-Clone/blob/master/LICENSE)

## Collaborate
For any collaborations, reach me on [okongofaith3@gmail.com]()