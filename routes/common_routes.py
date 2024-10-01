# routes/common_routes.py
from flask import Blueprint, render_template, session, redirect, url_for
common_bp = Blueprint('common_bp', __name__)

@common_bp.route('/')
def home():
    return render_template('home.html')

@common_bp.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', user_name=session['user_name'], role=session['user_role'])
