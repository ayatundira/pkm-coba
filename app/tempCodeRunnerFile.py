import os
from flask import Blueprint, render_template, redirect, url_for, session, request, Flask
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

#Halaman Login Executive
@routes.route('/login/executive', methods=['GET', 'POST'])
def login_executive():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Debug print untuk melihat nilai username dan password
            print(f"Attempting login with username: {username}")
            
            cursor.execute("SELECT * FROM USERS WHERE Username = ? AND Password = ?", 
                         (username, password))
            user = cursor.fetchone()
            
            # Debug print untuk melihat hasil query
            print(f"Query result: {user}")
            
            if user:
                session.clear()
                session['user'] = 'Executive Director'
                session['user_id'] = user[0]  # Pastikan ini sesuai dengan kolom ID di database
                print(f"Session after login: {session}")  # Debug print
                return redirect(url_for('routes.executive_dashboard'))
            else:
                return render_template('login_executive.html', 
                                     error="Invalid username or password")
        except Exception as e:
            print(f"Error during login: {e}")  # Debug print
            return render_template('login_executive.html', 
                                 error="Database error. Please try again.")
        finally:
            cursor.close()
            conn.close()
            
    return render_template('login_executive.html')

db = SQLAlchemy()
#executive_dashboard
@routes.route('/executive/dashboard')
def executive_dashboard():
    print(f"Current session: {session}")  # Debug print
    
    if 'user' not in session or session['user'] != 'Executive Director':
        print("Session check failed")  # Debug print
        return redirect(url_for('routes.login'))
    
    return render_template('executive_dashboard.html')

#search_shows
@routes.route('/search_shows', methods=['GET'])
def search_shows():
    search_query = request.args.get('query', '')
    if not search_query:
        return redirect(url_for('routes.executive_dashboard'))
    
    shows = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Search query with JOIN untuk mendapatkan nama status dan type
        search_sql = """
            SELECT 
                s.show_id,
                s.name,
                s.overview,
                s.original_name,
                s.popularity,
                s.in_production,
                s.episode_run_time,
                st.status_name,
                t.type_name
            FROM SHOWS s
            LEFT JOIN STATUS st ON s.status_id = st.status_id
            LEFT JOIN TYPES t ON s.type_id = t.type_id
            WHERE s.name LIKE @search_query
            OR s.original_name LIKE @search_query
            OR s.overview LIKE '%' + @search_query + '%'
        """
        search_pattern = f'%{search_query}%'

         # Debug prints
        print("Search Query:", search_query)
        print("SQL Query:", search_sql)
        
        cursor.execute(search_sql, (search_pattern, search_pattern, search_pattern))

        # Fetch results
        shows = cursor.fetchall()
        
        # Debug hasil
        print(f"Found {len(shows)} shows")
        if shows:
            print("First show found:", shows[0]) 

    except Exception as e:
        print(f"Database error: {e}")
        shows = []
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    
    return render_template('search_shows.html', shows=shows, search_query=search_query)

# Logout Executive
@routes.route('/executive/logout')
def logout_executive():
    session.pop('user', None)
    return redirect(url_for('routes.login'))

# Halaman Login Producer
@routes.route('/login/producer', methods=['GET', 'POST'])
def login_producer():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Cek credentials di database
            cursor.execute("SELECT * FROM USERS WHERE Username = ? AND Password = ?", 
                         (username, password))
            user = cursor.fetchone()
            
            if user:
                session.clear()
                session['user'] = 'Producer'
                session['user_id'] = user.id  # Simpan ID user di session
                return redirect(url_for('routes.producer_dashboard'))
            else:
                return render_template('login_producer.html', 
                                     error="Invalid username or password")
        except Exception as e:
            return render_template('login_producer.html', 
                                 error="Database error. Please try again.")
        finally:
            cursor.close()
            conn.close()
            
    return render_template('login_producer.html')


# Dashboard Producer
@routes.route('/producer/dashboard')
def producer_dashboard():
    if 'user' not in session or session['user'] != 'Producer':
        return redirect(url_for('routes.login'))
        
    # Ambil data user dari database
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            user_id = session.get('user_id')
            cursor.execute("SELECT Username FROM LOGIN_PRODUCER WHERE ID = ?", (user_id,))
            user_data = cursor.fetchone()
            
            # Pass username ke template
            return render_template('producer_dashboard.html', 
                                username=user_data[0] if user_data else "Unknown")
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('routes.login'))
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('routes.login'))

# Logout Producer
@routes.route('/producer/logout')
def logout_producer():
    session.pop('user', None)
    return redirect(url_for('routes.login'))

#read SHows
@routes.route('/view_shows_pro')
def view_shows_pro():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT TOP 1000
            s.show_id, 
            s.name, 
            s.pupularity, 
            s.episode_run_time AS episodes, 
            st.status_name AS status, 
            t.type_name AS type
        FROM SHOWS s
        LEFT JOIN STATUS st ON s.status_id = st.status_id
        LEFT JOIN TYPES t ON s.type_id = t.type_id
        LEFT JOIN AIR_DATES ad ON s.show_id = ad.show_id AND ad.is_first = 1
        ORDER BY s.pupularity DESC;
    """
    cursor.execute(query)
    shows = cursor.fetchall()
    conn.close()

    # Convert ke dictionary untuk passing ke template
    shows_list = [
        {
            "id": row.show_id,
            "name": row.name,
            "popularity": row.pupularity,
            "episodes": row.episodes,
            "status": row.status,
            "type": row.type,
        }
        for row in shows
    ]

    return render_template('view_shows.html', shows=shows_list)



if __name__ == '__main__':
    app.run(debug=True)
