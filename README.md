# CRUD - Ajax modal forms (django & jquery)
Django CRUD Ajax CBV, JQuery
<br />
inspired by https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html
<br />
used packages:
+ django-bootstrap-datepicker-plus - https://pypi.org/project/django-bootstrap-datepicker-plus/
+ toastr - a Javascript library for non-blocking notifications - https://github.com/CodeSeven/toastr
+ ajax multiple files upload - https://github.com/blueimp/jQuery-File-Upload
<br />
## How to use it

```bash
# Get the code
git clone https://github.com/egursu/django-modal-ajax-crud.git
cd django-modal-ajax-crud

# Virtualenv modules installation (Unix based systems)
python3 -m venv venv
source ./venv/bin/activate

# Virtualenv modules installation (Windows based systems)
# virtualenv env
# .\env\Scripts\activate

# Install modules - SQLite Storage
pip3 install -r requirements.txt

# Login
Username: admin
Password: crudajax

# Start the application (development mode)
python3 manage.py runserver # default port 8000

# Start the app - custom port
# python manage.py runserver 0.0.0.0:<your_port>

# Access the web app in browser: http://127.0.0.1:8000/
```
<br />
