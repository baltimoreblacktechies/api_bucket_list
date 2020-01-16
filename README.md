# API Bucket List

This API powers the backend of a Bucket List app. What is a bucket list app you ask? Basically a 
TODO List for things to do before you kick the bucket. This API supports all the REST verbs for 
performing actions against the database

| Action   | HTTP Verb   | Description                   |
| -------- |:-----------:| -----------------------------:|
| Create   | POST        | Create a new bucket list item |
| Read     | GET         | Get a bucket list item        |
| Update   | PUT         | Update a bucket list item     |
| Delete   | DELETE      | Delete a bucket list item     |

## Building Blocks

### Flask

Flask is a lightweight `WSGI`_ web application framework. It is designed
to make getting started quick and easy, with the ability to scale up to
complex applications.

* Website: https://palletsprojects.com/p/flask/
* Documentation: https://flask.palletsprojects.com/

### Connexion

Connexion is a framework that automagically handles HTTP requests based on `OpenAPI Specification`_
(formerly known as Swagger Spec) of your API described in `YAML format`_. Connexion allows you to
write an OpenAPI specification, then maps the endpoints to your Python functions

* http://connexion.readthedocs.org/en/latest/

### SQLAlchemy

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper
that gives application developers the full power and
flexibility of SQL.

* http://www.sqlalchemy.org/docs/

### Marshmallow: simplified object serialization

**marshmallow** is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.


## Notes
This assumes the user is using a Python version > 3.8

The requirements.txt file should list all Python libraries that your project depend on, 
and they will be installed using:

```pip3 install -r requirements.txt```