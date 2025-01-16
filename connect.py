import pyodbc
import os
from dotenv import load_dotenv

def create_connection():
    # load environment variables
    load_dotenv()
    
    # get connection details from .env
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    
    try:
        # Gunakan Windows Authentication
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            f'SERVER={server};'
            f'DATABASE={database};'
            'Trusted_Connection=yes;'  # Gunakan Windows Authentication
        )
        print("Successfully connected to database!")
        return conn
    except pyodbc.Error as e:
        print(f'Error: {e}')
        print('Failed to connect to the database.')
        return None

# Test koneksi
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.close()
        conn.close()