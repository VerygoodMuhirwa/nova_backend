import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("sensor_data", self.channel_name)
        await self.accept()
        print("WebSocket connection established")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("sensor_data", self.channel_name)
        print("WebSocket connection closed")

    async def send_sensor_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
        print(f"Sent data: {data}")
