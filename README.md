# get_xpath_from_url_django
## Create virtual environment
```
$ virtualenv venv
```
```
$ source venv/bin/activate
```
```
$ pip install -r requirements.txt
```
## Run the app
```
$ python3 manage.py runserver
```
## How to test the API
```
$ curl http://127.0.0.1:8000/get_xpath/ -H "Content-Type: application/json" -d '{"url": "https://google.com"}'
```
## Config file
 get_xpath_from_url_django/config.py
```
TAGS = ["input", "textarea", "select", "button", "a"]

ATTRIBUTES_PRIORITY = [
    "id",
    "name",
    "placeholder",
    "value",
    "title",
    "type",
    "href",
    "class",
]

SHOW_HIDDEN_ELEMENTS = False
```