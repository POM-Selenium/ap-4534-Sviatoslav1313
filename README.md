# Django_View-Templates

## install requirement project's packages

```commandline
pip install -r requirements.txt
```

## Run project

Go to the folder with manage.py file, run library
```commandline
python manage.py migrate 
```

```commandline
python manage.py runserver
```

## Run tests

There are no tests.

Everything is at your discretion and the feeling of beauty :)

**_As a result of this sprint ( except fot the code in  repository) you should have a short video (2-10min) that shows functionality of the app._**

## Tasks

Create the appropriate views and templates for:

**Do not use django forms, use only HTML forms!**

(if necessary, you can modify the models)

auth
* Provide the ability to register the user as a librarian or as an ordinary user (guest)
* Provide the ability to log in (guest)
* Provide the ability to Log out (authorized user)

books  (admin/user)

* show information about all books (admin/user)
* provide an opportunity to view a specific book (admin/user);
* provide the ability to filter books by various criteria (author, title, etc.) (admin/user);
* show all books provided to a specific user (by id) (admin);

users  (admin)

* show information about all users (admin/user)
* provide an opportunity to view a specific user (admin/user)

orders  (admin)

* show information about all orders (admin)
* show information about all my orders (user)
* provide an opportunity to create an order (user)
* provide an opportunity to close the order  (admin)

authors  (admin)

* show information about all authors (admin)
* provide an opportunity to create a new author  (admin)
* provide the ability to remove the author if he is not attached to any book (admin)
