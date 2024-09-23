<h1> online programming course platform </h1>
django project for term 4 university


<h2> creating a  Virtual environment </h2>

<h3> Linux </h3>

``` console
python -m venv venv
source venv\bin\activate
```
<h3> Windows  </h3>

``` console
py  -m venv venv
venv\Script\activate
```
<h2> install dependencies </h2>

``` console
pip install -r requirements.txt
```

<h2> start a new project </h2>

<h3> create a django project</h3>

``` console 
django-admin startproject project_name
```
<h3> database migrations </h3>

``` console
python manage.py makemigrations
python manage.py migrate
```

<h2> create SuperUser </h2>

``` console
python manage.py createsuperuser 
```
<h2> Run on localhost </h2>

``` console
python manage.py runserver
```
