from api import api
from flask import Flask, render_template, request, flash, redirect, url_for
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
print(app.config)
app.register_blueprint(api, url_prefix='/api')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', token='test')
