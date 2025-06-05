#!/usr/bin/python3
"""Starts the web app"""
from flask import Flask, render_template
from urllib.parse import unquote

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays the Hello HBNB"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """Returns the HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def display_c(text):
    """Replace underscores with spaces"""
    text = unquote(text).replace('_', ' ')
    return 'C {}'.format(text)


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python(text):
    """Replace underscores with spaces"""
    text = unquote(text).replace('_', ' ')
    return 'Python {}'.format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def display_number(n):
    """Display a number only if it is an integer"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def display_number_template(n):
    """Display a number only if it is an integer"""
    return render_template('5-number.html', n=n)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
