# import os

# Database configuration
# config.py

class Config:
    SECRET_KEY = 'your_secret_key_here'
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',        # Replace with your MySQL username
        'password': 'example', # Replace with your MySQL password
        'database': 'pembayaran_listrik' # Replace with your actual database name
    }

# Assign db_config for backward compatibility
db_config = Config.DB_CONFIG
