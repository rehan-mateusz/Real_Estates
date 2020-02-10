[HomePageSS1](/ss1.png)

# Real_Estates

Real estates is a web application for listing real estate and communication between users.

# Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.
```
$ pip install Python==3.5.3
$ pip install Django==2.2.4
$ pip install django-bootstrap3==11.1.0
$ pip install django-filter==2.2.0
```

Web app for CRUD real estates offers and user-to-user messaging system build with Django 2.2

This web app allows guests to view list of all created offers or filtered list of offers as well as detailed views of single offers.
Guest may also register an account (with default user model).

Registered users can create their own offers with limited number of images attached. Users can also update and delete their own offers. 
While in a particular offers details page, one can send a message to its owner. 
User sees a number of messages and unread messages next to "Inbox" url. While in inbox user sees a list of messages send by other users
(but only last message of every of the users). By clicking on a message from a particular user, one can see a chat view with that person
and is able to reply.
User can also edit additional information (like contact data) so it appears on every offer that user creates.

