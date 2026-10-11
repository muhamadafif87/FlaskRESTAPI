from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Initialize SQLAlchemy sebagai ORM
# fyi: ORM (Object-Relational Mapping) is a programming technique 
# that allows you to interact with a relational database 
# using the object-oriented logic of your programming language, 
# instead of writing raw SQL queries. SQLAlchemy is a highly popular, 
# open-source SQL toolkit and ORM designed specifically for Python

db = SQLAlchemy(model_class=Base)
jwt = JWTManager()
