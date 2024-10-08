import json
import asyncio
import cv2 as cv
import base64
import os
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from sensorapp.video_capture import play_alert_sound

# Setup logging
logging.basicConfig(level=logging.INFO)

# Get the base directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths to model files
faceProto = os.path.join(BASE_DIR, "../sensorapp/opencv_face_detector.pbtxt")
faceModel = os.path.join(BASE_DIR, "opencv_face_detector_uint8.pb")

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import SensorData  # Import your sensor data model

logging.basicConfig(level=logging.INFO)

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import SensorData
from asgiref.sync import sync_to_async

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from datetime import datetime


class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("sensor_data_group", self.channel_name)
        await self.accept()
        print("Connection established.")
        await self.send_sensor_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("sensor_data_group", self.channel_name)
        print(f"Disconnected with close code: {close_code}")

    async def receive(self, text_data):
        print(f"Data received: {text_data}")
        await self.send_sensor_data()

    async def sensor_data_update(self, event):
        if 'sensor_data' in event:
            sensor_data = event['sensor_data']
            await self.send(text_data=json.dumps({
                'sensor_data': sensor_data
            }))
        else:
            print("No 'sensor_data' key in the event")

    async def send_sensor_data(self):
        sensor_data_list = await sync_to_async(SensorData.get_all_data)()
        print(f"Number of records fetched: {len(sensor_data_list)}")

        grouped_sensor_data = {}

        for data in sensor_data_list:
            sensor_name = data.get("sensorName")
            sensor_id = data.get("sensorId")

            if sensor_name not in grouped_sensor_data:
                grouped_sensor_data[sensor_name] = []

            if sensor_name.lower() == 'Humidity_sensor':
                humidity_group = next(
                    (group for group in grouped_sensor_data[sensor_name] if group['sensorId'] == sensor_id),
                    None
                )

                if humidity_group is None:
                    humidity_group = {
                        "sensorId": sensor_id,
                        "data": []
                    }
                    grouped_sensor_data[sensor_name].append(humidity_group)

                # Append the temperature and moisture values instead of 'value'
                humidity_group['data'].append({
                    "user": data.get("user"),
                    "location": data.get("location"),
                    "physicalQuantity": data.get("physicalQuantity"),
                    "temperatureValue": data.get("temperatureValue"),
                    "moistureValue": data.get("moistureValue"),
                    "timestamp": data.get("timestamp")
                })
            else:
                # For other sensor types, include temperature and moisture values if present
                grouped_sensor_data[sensor_name].append({
                    "user": data.get("user"),
                    "location": data.get("location"),
                    "physicalQuantity": data.get("physicalQuantity"),
                    "temperatureValue": data.get("temperatureValue", None),
                    "moistureValue": data.get("moistureValue", None),
                    "timestamp": data.get("timestamp")
                })

        # Print the grouped data before sending
        print(f"Sending sensor data: {grouped_sensor_data}")

        # Send the grouped sensor data over the WebSocket
        await self.send(text_data=json.dumps({
            "sensor_data": grouped_sensor_data
        }))

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logging.info("Video WebSocket connection established.")

        # Start the video streaming task
        asyncio.create_task(self.video_stream())

    async def disconnect(self, close_code):
        logging.info("Video WebSocket connection closed.")

    async def receive(self, text_data):
        data = json.loads(text_data)

    async def video_stream(self):
        cap = cv.VideoCapture(0)  # Use webcam

        # Load the face detection model using the defined paths
        faceNet = cv.dnn.readNet(faceModel, faceProto)
        faceNet.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)

        while True:
            hasFrame, frame = cap.read()
            if not hasFrame:
                logging.warning("Failed to grab frame.")
                break

            frameFace, bboxes = self.get_face_box(faceNet, frame)

            # Encode frame as JPEG and send to the client
            _, buffer = cv.imencode('.jpg', frameFace)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            await self.send(text_data=json.dumps({'frame': jpg_as_text}))
            logging.info("Sent frame to frontend.")

            # Play alert sound if faces detected
            if bboxes:
                logging.info("Faces detected, playing alert sound.")
                play_alert_sound()

            await asyncio.sleep(0.03)  # Control the frame rate (30 FPS)
        cap.release()

    def get_face_box(self, net, frame, conf_threshold=0.5):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        blob = cv.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], True, False)
        net.setInput(blob)
        detections = net.forward()
        bboxes = []

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                bboxes.append([x1, y1, x2, y2])
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return frame, bboxes
