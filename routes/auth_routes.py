# routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modules.auth import authenticate_user, logout_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate_user(username, password):
            flash('Login successful!', 'success')
            return redirect(url_for('common_bp.dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # Logout logic
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
