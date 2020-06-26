from flask import Flask, Blueprint
from api.api import api


app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def route():
    return 'hai'


if __name__ == "__main__":
    app.run(debug=True)