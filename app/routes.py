import os
import hashlib
from flask import Blueprint, render_template, redirect, url_for, session, request, Flask, flash
import pyodbc  # Untuk koneksi ke database
from werkzeug.security import check_password_hash 
from flask import render_template, request
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy
from flask import app
from flask import render_template, request, redirect, url_for, session
from sqlalchemy import or_
from models import db, Shows  # Import db and Shows from your models file



# Create a blueprint
routes = Blueprint('routes', __name__)

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        f'SERVER={os.getenv("DB_SERVER")};'
        f'DATABASE={os.getenv("DB_NAME")};'
        'Trusted_Connection=yes;'
    )
    return conn

@routes.route('/')
def index():
    return redirect(url_for('routes.login'))


# Halaman Login Utama
@routes.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
