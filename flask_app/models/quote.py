from flask import flash
import re
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Quote:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.phone_number = data['phone_number']
        self.description = data['description']
        self.best_time_to_call = data['best_time_to_call']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO quotes (name, email, phone_number, description, best_time_to_call, created_at, updated_at)
            VALUES (%(name)s, %(email)s, %(phone_number)s, %(description)s, %(best_time_to_call)s, NOW(), NOW());
            """
        return connectToMySQL("first_project_schema").query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM quotes;"
        results = connectToMySQL("first_project_schema").query_db(query)
        quotes = []
        for row in results:
            quotes.append(cls(row))

        return quotes

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM quotes WHERE id = %(id)s;"
        results = connectToMySQL("first_project_schema").query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
                UPDATE quotes SET name = %(name)s, email = %(email)s, phone_number = %(phone_number)s, description = %(description)s,
                best_time_to_call = %(best_time_to_call)s, updated_at = NOW() WHERE id = %(id)s;
        """
        return connectToMySQL("first_project_schema").query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM quotes WHERE id = %(id)s;"
        return connectToMySQL("first_project_schema").query_db(query, data)

    @staticmethod
    def validate(post_data):
        is_invalid = True

        if len(post_data['name']) < 2:
            flash("Name must be at least 2 characters!")
            is_invalid = False
        
        if len(post_data['email']) < 2:
            flash("Email must be valid!")
            is_invalid = False

        if len(post_data['phone_number']) < 8:
            flash("Phone number must be valid!")
            is_invalid = False
        
        if len(post_data['description']) < 2:
            flash("Description must be at least 5 characters!")
            is_invalid = False
        
        return is_invalid
