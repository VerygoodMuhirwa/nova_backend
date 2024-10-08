# models.py

from django.utils import timezone
from nova_backend.db_connection import MongoConnection  # Import the connection class


class SensorData:
    def __init__(self, user, sensorName, sensorId, location, physicalQuantity, moistureValue, temperatureValue, timestamp=None):
        self.user = user
        self.sensorId = sensorId
        self.sensorName = sensorName
        self.location = location
        self.physicalQuantity = physicalQuantity
        self.moistureValue = moistureValue
        self.temperatureValue = temperatureValue
        self.timestamp = timestamp if timestamp else timezone.now()

    def save(self):
        # Get MongoDB collection
        connection = MongoConnection()
        collection = connection.get_collection('sensor_data')

        # Convert object to a dictionary and insert it into MongoDB
        data = {
            "user": self.user,
            "sensorName": self.sensorName,
            "sensorId": self.sensorId,
            "location": self.location,
            "temperatureValue": self.temperatureValue,
            "moistureValue": self.moistureValue,
            "physicalQuantity": self.physicalQuantity,
            "timestamp": self.timestamp,
        }

        collection.insert_one(data)  # Insert into MongoDB

    def __str__(self):
        return f"Sensor: {self.sensorName} | temperatureValue: {self.temperatureValue} | moistureValue:{self.moistureValue} Timestamp: {self.timestamp}"

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
