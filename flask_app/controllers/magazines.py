# magazines.py

from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.magazine import Magazine

@app.route('/magazines')
def get_all_magazines():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'invalid_credentials_error')
        return redirect('/')
    magazines = get_all_magazines()
    return render_template('magazines.html', magazines=magazines)

@app.route('/magazines/add_magazine')
def get_add_magazine_form():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'invalid_credentials_error')
        return redirect('/')
    return render_template('add_magazine_form.html')

@app.route('/magazines/add/process', methods=['POST'])
def post_new_magazine():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'invalid_credentials_error')
        return redirect('/')
    if not Magazine.validate_magazine(request.form):
        return redirect('/magazines/add_magazine')
    Magazine.save(request.form)
    return redirect(f'/dashboard/{session["user_id"]}')

@app.route('/magazines/<int:id>')
def get_magazines_page(id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'invalid_credentials_error')
        return redirect('/')
    magazine = Magazine.get_one_magazine(id)
    if not magazine:
        return render_template('no_magazine_found_page.html')
    return render_template('magazine.html', magazine=magazine)

@app.route('/magazines/<int:id>/delete', methods=['POST'])
def delete_magazine(id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'invalid_credentials_error')
        return redirect('/')
    Magazine.delete_magazine(id)
    return redirect(f'/dashboard/{session["user_id"]}')

@app.route('/magazines/no_magazine_found')
def no_magazine_found():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'invalid_credentials_error')
        return redirect('/')
    return render_template('no_magazine_found_page.html', magazines=None)