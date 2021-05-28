![HomePageSS1](/ss1.PNG)

# Real_Estates
Real estates is a web application for listing real estate and communication between registered users. Deployed at [http://kulas971.pythonanywhere.com](http://kulas971.pythonanywhere.com/)

**Guests can:**
- See the list of all offers and filter this list 
- See detailed view of particular offer
- See all offers of particular user
- Register an account
- Log in

**Registered users can:**
- Create their own offers
- Edit their own offers
- Delete their own offers
- Send message to an author of a particular offer
- Read all received messages 
- Reply to received messages
- Change profile info
- Log out

**Admin can:**
- use admin panel (django admin)

# How to use
After cloning the repository

**Start with docker:**

cd to /Real_estates and use docker-compose
```
docker-compose up
```
**Start with Python:**

Preferably create a virtual environment.

cd to /Real_estates/estate_pro
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.
```
pip install -r requirements.txt
```
With requirements installed you can run the app:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


# Test accounts
If you don't want to register an account (you can use fake email, no confirmation needed), you can use one of two test accounts:
- testuser1 / Testpassword1
- testuser2 / Testpassword2

 # Run tests
 cd into /Real_Estates/estate_pro and type 
 ```
pytest
```

