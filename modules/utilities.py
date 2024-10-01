# modules/utilities.py
import mysql.connector
from config import db_config

def get_db_connection():
    """Utility function to establish a database connection."""
    return mysql.connector.connect(**db_config)
    return connection
