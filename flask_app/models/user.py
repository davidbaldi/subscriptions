# user.py

from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import bcrypt
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    db = 'magazines'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

# Create a new user
    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        return connectToMySQL(cls.db).query_db(query, data)

# Get one user by their id
    @classmethod
    def get_user_by_id(cls, data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

# Get one user by their email
    @classmethod
    def get_user_by_email(cls, data):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return cls(results[0])

# Update user info
    @classmethod
    def update_user_info(cls, data):
        query = """
                UPDATE users
                SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query, data)

# Validate registration
    @staticmethod
    def validate_registration(user):
        is_valid = True
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken. Choose another!", 'registration_error')
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters!", 'registration_error')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters!", 'registration_error')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email format!", 'registration_error')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters!", 'registration_error')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match!", 'registration_error')
            is_valid = False
        return is_valid

# Validate login
    @staticmethod
    def validate_login(user):
        is_valid = True
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """
        results = connectToMySQL(User.db).query_db(query, user)
        if not results:
            is_valid = False
            flash("Email not found!", 'login_error')
        if not bcrypt.check_password_hash(User(results[0]).password, user['password']):
            is_valid = False
            flash("Invalid password!", 'login_error')
        return is_valid

    @ staticmethod
    def validate_user_update(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters!", 'user_update_error')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters!", 'user_update_error')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email format!", 'user_update_error')
            is_valid = False
        return is_valid