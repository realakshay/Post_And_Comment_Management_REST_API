## Posts_And_Comment_Management_REST_API

##### Description : This project is just a simple advance api for posts and comments on application management with email confirmation.
Its just like social media post where we can comment on post. Here also like that. We can manage that comments here.

###### Modules : 
    User Registration, User Login, User Logout, Make fresh token, User Authentication- Manually and with confirmation mail, 
    User Blacklist, Posts insert, delete, update and get then comments of specific post management

        libs -> This package contain mailgun template and string file management
        modules -> This package contain all the db models
        resources -> This package contain all the resource class and requests
        schemas -> This package contain all schema class to manage database models
        strings -> This package is for localization and internationalization purpose

#### Tools : 

        1.Flask
        2.Flask-RESTful
        3.Flask-jwt-extended
        4.Flask-sqlalchemy
        5.Flask-marshmallow
        6.Marshmallow
        7.Marshmallow-sqlalchemy
        

#### .env.example
        Here .env.example file shows thats security of some information. You have to create .env file and store all credentials in it so important libraries will work fine.


#### Email verification by using :

        1.Mailgun
     
#### Localization and Internationalization

        Here strings.json file created to manage all the messages and information. We can change language as user want.
        
#### How to run this project

##### $python app.py

#### This will run on http://127.0.0.1:5555
