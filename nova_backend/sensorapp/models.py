# models.py

from django.utils import timezone
from nova_backend.db_connection import MongoConnection  # Import the connection class


class SensorData:
    def __init__(self, user, sensorName, location, physicalQuantity, value, timestamp=None):
        self.user = user
        self.sensorName = sensorName
        self.location = location
        self.physicalQuantity = physicalQuantity
        self.value = value
        self.timestamp = timestamp if timestamp else timezone.now()

    def save(self):
        # Get MongoDB collection
        connection = MongoConnection()
        collection = connection.get_collection('sensor_data')

        # Convert object to a dictionary and insert it into MongoDB
        data = {
            "user": self.user,
            "sensorName": self.sensorName,
            "location": self.location,
            "physicalQuantity": self.physicalQuantity,
            "value": self.value,
            "timestamp": self.timestamp,
        }

        collection.insert_one(data)  # Insert into MongoDB

    def __str__(self):
        return f"Sensor: {self.sensorName} | Value: {self.value} | Timestamp: {self.timestamp}"

    @staticmethod
    def get_all_data():
        # Fetch all documents in the collection
        connection = MongoConnection()
        collection = connection.get_collection('sensor_data')
        return list(collection.find({})) if collection else []

    @staticmethod
    def find_by_sensor_name(sensor_name):
        # Query to find a document by the sensor name
        connection = MongoConnection()
        collection = connection.get_collection('sensor_data')
        return collection.find_one({"sensorName": sensor_name}) if collection else None
