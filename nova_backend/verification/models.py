# models.py

from nova_backend.db_connection import MongoConnection  # Import the MongoDB connection class
from user.models import User  # Assuming you're referencing the User model

class VerificationCode:
    def __init__(self, email, code):
        self.email = email
        self.code = code

    def save(self):
        # Get MongoDB collection for verification codes
        connection = MongoConnection()
        collection = connection.get_collection('verification_codes')

        # Convert the object to a dictionary and insert it into MongoDB
        verification_data = {
            "email": self.email,
            "code": self.code
        }

        collection.insert_one(verification_data)  # Insert into MongoDB

    def __str__(self):
        # Find the user associated with this email for display purposes
        user = User.find_by_email(self.email)
        return f"{self.code} for {user['username']}" if user else f"{self.code} for unknown user"

    @staticmethod
    def find_by_email(email):
        # Query to find a verification code by email
        connection = MongoConnection()
        collection = connection.get_collection('verification_codes')
        return collection.find_one({"email": email})

    @staticmethod
    def find_by_code(code):
        # Query to find a verification code by code
        connection = MongoConnection()
        collection = connection.get_collection('verification_codes')
        return collection.find_one({"code": code})

    def _id(self):
        # Retrieve the MongoDB document ID
        connection = MongoConnection()
        collection = connection.get_collection('verification_codes')
        verification_code = collection.find_one({"email": self.email})
        return str(verification_code['_id']) if verification_code else None
