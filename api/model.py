from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

model = Blueprint('model', __name__, static_folder='static', template_folder='templates')
