Works Single View
=================

This is a python 3 project.

Python Dependencies
-------------------

The python dependencies are listed in `requirements.txt`. Install them in your
virtual environment via:

```sh
pip install -r requirements.txt
```

Setting the database
--------------------

https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04

```
sudo su postgres
psql
CREATE USER bmat WITH PASSWORD 'bmat';
ALTER USER bmat CREATEDB;
ALTER ROLE bmat SET client_encoding TO 'utf8';
ALTER ROLE bmat SET default_transaction_isolation TO 'read committed';
ALTER ROLE bmat SET timezone TO 'UTC';
CREATE DATABASE bmat OWNER bmat;
GRANT ALL PRIVILEGES ON DATABASE bmat TO bmat;
\q
exit
```

Running Tests
-------------

First create the test database

```
sudo su postgres
psql
CREATE DATABASE test_bmat OWNER bmat;
GRANT ALL PRIVILEGES ON DATABASE test_bmat TO bmat;
\q
exit
```

I'm using `pytest-django` for running the tests. Run the tests with `pytest`:

```sh
pytest
```

Importing works from a CSV file using the `import_works` management command
---------------------------------------------------------------------------

A custom management command exists to import works metadata from a CSV file.

```sh
python manage.py import_works <file>
```

API Description
---------------

```
GET /works/

POST /works/

PATCH /works/<work_uid>/

GET /works/<work_uid>/

DELETE /works/<work_uid>/

GET /works/csv

POST /works/csv
```


Possible improvements
---------------------

* Pagination and filtering of API list returns
* Environment variables via django-environ and database configration via DATABASE_URL
* If this were a project to be used in production I'd use https://github.com/pydanny/cookiecutter-django
  to set the project's scaffolding.
* Authentication for API calls
