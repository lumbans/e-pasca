# modules/user.py
from modules.utilities import get_db_connection
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

def get_all_users():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id_user, username, nama_admin, id_level from user")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return users

def add_user(username, password, role):
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Inserting user data into the database
        cursor.execute("INSERT INTO user (username, password, id_level) VALUES (%s, %s, %s)", (username, hashed_password, role))
        
        db.commit()
        flash('User added successfully!', 'success')
        
    except Exception as e:
        # Handle any errors during insertion
        db.rollback()
        flash(f'Error adding user: {str(e)}', 'danger')
        
    finally:
        # Ensure the database connection is closed
        cursor.close()
        db.close()

def change_user_password(user_id, old_password, new_password, confirm_password):
    if new_password != confirm_password:
        flash("New passwords do not match", "danger")
        return False
    
    db = get_db_connection()
    cursor = db.cursor()
    
    # Verify old password
    cursor.execute("SELECT password FROM user WHERE id_user = %s", (user_id,))
    user = cursor.fetchone()
    
    if user and user[0] == old_password:
        # Update with new password
        cursor.execute("UPDATE user SET password = %s WHERE id_user = %s", (new_password, user_id))
        db.commit()
        
        cursor.close()
        db.close()
        
        flash("Password changed successfully!", "success")
        return True
    
    flash("Old password is incorrect", "danger")
    return False

def update_user(id_user, username, nama_admin, password, role):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE user SET username = %s, nama_admin = %s, password = %s, id_level = %s WHERE id_user = %s", (username, nama_admin, password, role, id_user))
    db.commit()
    cursor.close()
    db.close()
    flash('User updated successfully!', 'success')

def delete_user(id_user):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM user WHERE id_user = %s", (id_user,))
    db.commit()
    cursor.close()
    db.close()
    flash('User deleted successfully!', 'success')