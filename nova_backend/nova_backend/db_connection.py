
from pymongo import MongoClient
from django.conf import settings


# class MongoConnection:
#     def __init__(self):
#         self.client = None
#         self.db = None
#         self._connect()
#
#     def _connect(self):
#         try:
#             self.client = MongoClient(
#                 host="mongodb+srv://cluster0.c5iqqff.mongodb.net",  # Your MongoDB host URL
#                 username=settings.MONGO_DB_USERNAME,
#                 password=settings.MONGO_DB_PASSWORD,
#                 authSource="admin",
#                 authMechanism="SCRAM-SHA-1",
#             )
#             self.db = self.client[settings.MONGO_DB_NAME]
#             print("Successfully connected to MongoDB")
#         except Exception as e:
#             print(f"Error connecting to MongoDB: {e}")
#
#     def get_collection(self, collection_name):
#         """Get the MongoDB collection."""
#         return self.db[collection_name] if self.db else None


class MongoConnection:
    def __init__(self):
        self.client = None  # MongoDB client instance
        self.db = None      # Database instance
        self._connect()     # Establish a connection to local MongoDB

    def _connect(self):
        """Establish a connection to local MongoDB."""
        try:
            # Create a MongoDB client connecting to the local server
            self.client = MongoClient(
                host="localhost",  # Local MongoDB server
                port=27017,        # Default MongoDB port
            )
            self.db = self.client["nova_project"]           # Access the specified database (replace with your database name)
            print("Successfully connected to local MongoDB")       # Success message
        except Exception as e:
            print(f"Error connecting to local MongoDB: {e}")     # Error handling

    def get_collection(self, collection_name):
        """Get the MongoDB collection."""
        return self.db[collection_name] if self.db else None     # Return the specified collection if connected
