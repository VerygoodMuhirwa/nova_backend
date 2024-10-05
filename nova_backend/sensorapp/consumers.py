import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import SensorData
from asgiref.sync import sync_to_async


class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Connection established.")

        # Immediately send sensor data upon connection
        await self.send_sensor_data()

    async def disconnect(self, close_code):
        print(f"Disconnected with close code: {close_code}")

    async def receive(self, text_data):
        print(f"Data received: {text_data}")
        await self.send_sensor_data()

    async def send_sensor_data(self):
        # Use sync_to_async to perform synchronous DB operations in async context
        sensor_data_list = await sync_to_async(list)(SensorData.objects.all())

        # Debug: Print the number of records fetched
        print(f"Number of records fetched: {len(sensor_data_list)}")

        # Prepare data to be sent over the WebSocket
        sensor_data_response = [
            {
                "user": data.user,  # Access user properly
                "sensorName": data.sensorName,
                "location": data.location,
                "physicalQuantity": data.physicalQuantity,
                "value": data.value,
                "timestamp": data.timestamp.isoformat(),
            } for data in sensor_data_list
        ]

        # Print the data before sending
        print(f"Sending sensor data: {sensor_data_response}")

        # Send the sensor data over the WebSocket
        await self.send(text_data=json.dumps({
            "sensor_data": sensor_data_response
        }))
