# models.py

from  nova_backend.db_connection import MongoConnection  # Import the MongoConnection class

class User:
    def __init__(self, username, email, password, phoneNumber, photo=None):
        self.username = username
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber
        self.photo = photo if photo else 'https://icon-library.com/images/anonymous-avatar-icon/anonymous-avatar-icon-25.jpg'

    def save(self):
        # Get MongoDB collection
        connection = MongoConnection()
        collection = connection.get_collection('users')

        # Convert object to a dictionary and insert it into MongoDB
        user_data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "phoneNumber": self.phoneNumber,
            "photo": self.photo
        }

        collection.insert_one(user_data)  # Insert into MongoDB

    def __str__(self):
        return self.email

    @staticmethod
    def find_by_email(email):
        # Query to find a user by email
        connection = MongoConnection()
        collection = connection.get_collection('users')
        return collection.find_one({"email": email})

    @staticmethod
    def get_all_users():
        # Fetch all users in the collection
        connection = MongoConnection()
        collection = connection.get_collection('users')
        return list(collection.find({})) if collection else []
