# app/__init__.py
from flask import Flask

app = Flask(__name__, 
    template_folder='templates',  # karena kita sudah di dalam folder app
    static_folder='static')

from app import routes


