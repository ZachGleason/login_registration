from stat import FILE_ATTRIBUTE_OFFLINE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import session
from flask_app.models.user import User

class Product:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]

    @classmethod 
    def get_all(cls, data):
            query = "SELECT * FROM products;"
            results =  connectToMySQL("login_registration").query_db(query, data)
            return results

    @classmethod
    def add_product(cls, data):
        query = "INSERT INTO products (name, price) VALUES (%(name)s, %(price)s) WHERE user_id = "
        results =  connectToMySQL("login_registration").query_db(query, data)
        return results


