import sys
import os
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
