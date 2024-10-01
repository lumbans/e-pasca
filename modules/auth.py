# modules/auth.py
from modules.utilities import get_db_connection  # Adjust import paths if needed
from flask import flash, session

def authenticate_user(username, password):
    db = get_db_connection()
    cursor = db.cursor()
    
    # First, try to fetch user details from the 'user' table
    cursor.execute("SELECT id_user, username, password, id_level FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    # If user is found in the 'user' table
    if user:
        # Debugging: Print fetched data
        print(f"Fetched User: ID={user[0]}, Username={user[1]}, Password={user[2]}, Role={user[3]}")
        
        # Check if the password matches
        if user[2] == password:
            session['user_id'] = user[0]
            session['logged_in'] = True
            session['user_name'] = user[1]
            session['user_role'] = 'admin' if user[3] == 1 else 'operator'
            return True
    else:
        # If not found in 'user' table, try to fetch details from 'pelanggan' table
        cursor.execute("SELECT id_pelanggan, username, password, nama_pelanggan FROM pelanggan WHERE username = %s", (username,))
        pelanggan = cursor.fetchone()
        
        # If pelanggan is found
        if pelanggan:
            # Debugging: Print fetched data
            print(f"Fetched Pelanggan: ID={pelanggan[0]}, Username={pelanggan[1]}, Password={pelanggan[2]}, Nama={pelanggan[3]}")
            
            # Check if the password matches
            if pelanggan[2] == password:
                session['user_id'] = pelanggan[0]  # Store id_pelanggan in user_id for consistency
                session['logged_in'] = True
                session['user_name'] = pelanggan[3]
                session['user_role'] = 'pelanggan'
                session['id_pelanggan'] = pelanggan[0]  # Set id_pelanggan in session for pelanggan-specific actions
                return True
    
    # If no match found or password mismatch
    flash('Invalid credentials. Please try again.', 'danger')
    cursor.close()
    db.close()
    return False

def logout_user():
    session.clear()