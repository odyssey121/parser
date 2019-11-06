from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
# print(app.config)
from app.api import api 
app.register_blueprint(api, url_prefix = '/api')

from app import routes
