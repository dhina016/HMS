from flask import Flask, Blueprint

api = Blueprint('api', __name__, static_folder='static', template_folder='templates')

@api.route('/')
def check():
    return 'asaj'
