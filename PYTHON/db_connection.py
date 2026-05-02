# ============================================================
# db_connection.py
# Ket noi MySQL - localhost:3306, user=root, pass=123456
# ============================================================

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host':     'localhost',
    'port':     3306,
    'database': 'OnlineCourseDB',
    'user':     'root',
    'password': '123456',
    'charset':  'utf8mb4',
    'autocommit': False
}

def get_connection():
    """Tao ket noi toi MySQL, tra ve connection object hoac None neu loi."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"  [LOI KET NOI] {e}")
        return None

def close_connection(conn, cursor=None):
    """Dong cursor va connection an toan."""
    try:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    except Error:
        pass