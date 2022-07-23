# magazine.py

# Not using 'redirect'!
from flask import flash, redirect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Magazine:

    db = 'magazines'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.user_id = data['user_id']
        self.user = None

# Add a magazine
    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO magazines (title, description, user_id)
                VALUES (%(title)s, %(description)s, %(user_id)s);
                """
        return connectToMySQL(cls.db).query_db(query, data)

# Get all magazines
    @classmethod
    def get_all_magazines(cls):
        query = """
                SELECT * FROM magazines
                JOIN users ON magazines.user_id = users.id;
                """
        results = connectToMySQL(cls.db).query_db(query)
        magazines = []
        for row in results:
            magazine = cls(row)

            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }

            magazine.user = User(user_data)
            magazines.append(magazine)
        return magazines

# Get all magazines by user
    @classmethod
    def get_all_magazines_by_user_id(cls, user_id):
        # Needs dictionary?
        data = {
            'user_id': user_id
        }
        query = """
                SELECT * FROM magazines
                JOIN users ON magazines.user_id = users.id
                WHERE user_id = %(user_id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        magazines = []
        for row in results:
            if results:
                magazine = cls(row)

                user_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                }

                magazine.user = User(user_data)
                magazines.append(magazine)
            elif not results:
                return redirect('/magazines/no_magazine_found')
        return magazines

# Get one magazine
    @classmethod
    def get_one_magazine(cls, id):
        data = {
            'id': id
        }
        query = """
                SELECT * FROM magazines
                JOIN users ON user_id = users.id
                WHERE magazines.id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        # What if nothing shows up from the query? Would this next line fail?
        magazine = cls(results[0])
        user_data = {
                'id': results[0]['users.id'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'email': results[0]['email'],
                'password': results[0]['password'],
            }
        magazine.user = User(user_data)
        return magazine

# Delete a magazine
    @classmethod
    def delete_magazine(cls, id):
        data = {
            'id': id
        }
        query = """
                DELETE FROM magazines
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query, data)

# Is this set up to redirect to dashboard after adding magazine?
# Validate a magazine
    @staticmethod
    def validate_magazine(magazine):
        is_valid = True
        if len(magazine['title']) < 2:
            is_valid = False
            flash("Minimum 2 characters for magazine title!", 'add_magazine_error')
        if len(magazine['description']) < 10:
            is_valid = False
            flash("Minimum 10 characters for magazine description!", 'add_magazine_error')   
        return is_valid