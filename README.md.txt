# Condingal Tech Test

A project with the following APIS:
1. List All Comments Under A post
2. Add new comment/reply 
3. Edit existing comment
4. Create Support Tickets
5. Delete the full comment and its replies

## Steps To Run the Project


Clone the repo.

Create a virtualenv and activate it

cd into the folder

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt -
```bash
pip install -r requirements.txt
```

Make Migrations 
```bash
python manage.py makemigrations
```
```bash

python manage.py migrate
```
Run the server 
```bash
python manage.py runserver
```


## Routes


```
POST/DELETE - comment/<comment_id> Update or delete comment
POST- comments/create/<post_id> Add New comment to a post/ Post a reply to a comment 
GET - comments/view/<post_id> View all comments under a post
