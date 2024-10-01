# routes/user_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modules.user import get_all_users, add_user, update_user, delete_user, change_user_password

user_bp = Blueprint('user_bp', __name__)

# Add this route for manage_users
@user_bp.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        # Handle adding/updating user logic here
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        add_user(username, password, role)
        return redirect(url_for('user_bp.manage_users'))

    # Get the list of all users
    users = get_all_users()
    return render_template('manage_users.html', users=users)

@user_bp.route('/add_user', methods=['POST'])
def add_user_route():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('id_level')  # Make sure to use the correct field name

    # Add user logic (your add_user function should handle the insertion)
    add_user(username, password, role)
    
    flash('User added successfully!', 'success')
    return redirect(url_for('user_bp.manage_users'))

@user_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'logged_in' not in session:
        return redirect(url_for('auth_bp.login'))

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Assuming you have a function in your module to handle password change
        if change_user_password(session['user_id'], old_password, new_password, confirm_password):
            flash('Password changed successfully!', 'success')
            return redirect(url_for('common_bp.dashboard'))
        else:
            flash('Failed to change password. Please try again.', 'danger')
    
    return render_template('change_password.html')

@user_bp.route('/update_user', methods=['POST'])
def update_user_route():
    user_id = request.form['id_user']  # Make sure you have an input for id_user in your form
    username = request.form['username']
    nama_admin = request.form['nama_admin']
    password = request.form['password']
    role = request.form['id_level']  # Use 'id_level' here if that's your form's name attribute

    # Call your update function
    update_user(user_id, username, nama_admin, password, role)
    
    flash('User updated successfully!', 'success')
    return redirect(url_for('user_bp.manage_users'))

@user_bp.route('/delete_user/<int:id>', methods=['POST'])
def delete_user_route(id):
    delete_user(id)
    return redirect(url_for('user_bp.manage_users'))