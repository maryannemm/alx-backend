#!/usr/bin/env python3
from flask import Flask, render_template
from flask_babel import Babel, _

app = Flask(__name__)

class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(Config)
babel = Babel(app)

@app.route('/')
def index():
    return render_template('3-index.html', home_title=_("home_title"), home_header=_("home_header"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

