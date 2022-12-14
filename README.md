# ku-polls
[![Unittest](https://github.com/reviseUC73/ku-polls/actions/workflows/python-app.yml/badge.svg)](https://github.com/reviseUC73/ku-polls/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/reviseUC73/ku-polls/branch/master/graph/badge.svg?token=UMFYY8R20C)](https://codecov.io/gh/reviseUC73/ku-polls)

A web application for polls and survey at Kasetsart University

# Online Polls And Surveys

An application for conducting a poll or survey, written in Python using Django. It is based on the [Django Tutorial project][django-tutorial],
with additional functionality.

This application is part of the [Individual Software Process](https://cpske.github.io/ISP) course at Kasetsart University.

# Install and Run

first clone this repository by use this command
```
git clone https://github.com/reviseUC73/ku-polls.git
```
go to project directory
```
cd ku-polls
```
Start the virtual environment.

- on macos and linux
```
source env/bin/activate 
```
- on windows
```
. env/bin/activate
```
make sure that you install all the requirements by run this command, its can be whether pip, pip3
```
pip install -r requirements.txt
```
you have to create file name `.env`
file template looks like [sample.env](https://github.com/reviseUC73/ku-polls/blob/iteration3/mysite/sample.env) you can modify value and copy it into `.env`

Create `.env` and write.
```
SECRET_KEY = secret-key-value-without-quotes 
DEBUG = False
TIME_ZONE = Asia/Bangkok
```

Create a new database by running migrations the database.
```
python3 manage.py migrate
```
Import and Export the database.

Import the database python3 manage.py loaddata.

```
python3 manage.py loaddata data/polls.json data/users.json
```
Export the database `python3 manage.py dumpdata` (Optional). Try dump all polls data to a file (-o) named `polls.json`
```
python3 manage.py dumpdata --indent=2 -o polls.json polls
```
In this time you can run server by use command 
```
python manage.py runserver
```
but you have python3 use command
```
python3 manage.py runserver
```
next you go to `http://127.0.0.1:8000/` or `localhost:8000/` for application.

# Project Documents

All project documents are in the [Project Wiki](../../wiki/Home)

1. [Wiki Home](../../wiki/Home)
2. [Vision statement](../../wiki/Vision-Statement)
3. [Requirements](../../wiki/Requirements)
4. [Project Plan](../../wiki/Development%20Plan)
5. Iteration Plan

- [Iteration 1 Plan](https://github.com/reviseUC73/ku-polls/wiki/Iteration-1-Plan)
- [Iteration 2 Plan](https://github.com/reviseUC73/ku-polls/wiki/Iteration-2-Plan)
- [Iteration 3 Plan](https://github.com/reviseUC73/ku-polls/wiki/Iteration-3-Plan)
- [Iteration 4 Plan](https://github.com/reviseUC73/ku-polls/wiki/Iteration-4-Plan)


6. [Task Borad](https://github.com/users/reviseUC73/projects/3)
 
[django-tutorial]: https://docs.djangoproject.com/en/4.1/intro/tutorial01/
 
 # Running KU Polls
 Users provided by the initial data
 
 | Username  | Password  |
|-----------|-----------|
|   demo1   | demopass1 |
|   demo2   | demopass2 |
 
