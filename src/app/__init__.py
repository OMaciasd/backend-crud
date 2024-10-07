from . import routes
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

database_url = os.environ.get('TF_VAR_postgres_url')

if not database_url:
    raise ValueError(
        "The environment variable 'TF_VAR_postgres_url' is not set."
    )

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

try:
    db.engine.execute('SELECT 1')
    print("Database connection successful.")
except Exception as e:
    print("Error connecting to the database:", e)
