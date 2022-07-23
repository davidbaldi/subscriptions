# users.py

from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.controllers.magazines import get_all_magazines
from flask_app.models.magazine import Magazine
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
import bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def get_login_and_registration_form():
    return render_template('login_and_registration.html')

@app.route('/process_registration', methods=['POST'])
def process_registration():
    if not User.validate_registration(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.save(data)
    user = User.get_user_by_email(data)
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    return redirect(f'/dashboard/{session["user_id"]}')

@app.route('/process_login', methods=['POST'])
def process_login():
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.get_user_by_email(request.form)
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect(f'/dashboard/{session["user_id"]}')

@app.route('/dashboard/<int:id>')
def get_user_dashboard(id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'invalid_credentials_error')
        return redirect('/')
    magazines = Magazine.get_all_magazines()
    return render_template('dashboard.html', magazines=magazines)

@app.route('/users/<int:id>/update')
def get_update_user_form(id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'invalid_credentials_error')
        return redirect('/')
    magazines = Magazine.get_all_magazines_by_user_id(id)
    if not magazines:
        return redirect('/magazines/no_magazine_found')
    return render_template('update_user_page.html', magazines=magazines)

@app.route('/users/process_update', methods=['POST'])
def process_update():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'invalid_credentials_error')
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'id': session['user_id']
    }
    if not User.validate_user_update(data):
        return redirect(f'/users/{session["user_id"]}/update')
        # Don't forget to flash!
    User.update_user_info(data)
    flash("Preferences will be updated the next time you log in.", 'update_prompt')
    return redirect(f'/users/{session["user_id"]}/update')

@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')