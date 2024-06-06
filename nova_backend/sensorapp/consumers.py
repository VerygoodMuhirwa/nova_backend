import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("sensor_data", self.channel_name)
        await self.accept()
        print(f"WebSocket connection established for {self.channel_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("sensor_data", self.channel_name)
        print(f"WebSocket connection closed for {self.channel_name}")

    async def send_sensor_data(self, event):
        data = event.get('data')  # Using .get() for safe access
        if data is not None:
            try:
                await self.send(text_data=json.dumps(data))
                print(f"Sent data: {data}")
            except Exception as e:
                print(f"Error sending data: {e}")
        else:
            print("No data to send")
