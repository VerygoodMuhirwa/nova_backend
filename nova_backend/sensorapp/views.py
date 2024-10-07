import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views import View
from .models import SensorData  # Import your custom SensorData class
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone


@csrf_exempt
def fetch_and_receive_data(request):
    if request.method == "POST":
        try:
            channel_id = '2511877'
            read_api_key = 'YX33ECEWQJ1PXWKJ'
            url = f'https://api.thingspeak.com/channels/{channel_id}/feeds/last.json?api_key={read_api_key}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if 'field1' in data and 'field2' in data:
                    temperature = float(data['field1'])
                    moisture = float(data['field2'])
                    timestamp = timezone.now().isoformat()

                    # Save data to MongoDB
                    sensor_data = SensorData(
                        user='default_user',  # Adjust as necessary
                        sensorName='ThingSpeak Sensor',  # Adjust as necessary
                        location='Unknown',  # Adjust as necessary
                        physicalQuantity='Temperature/Moisture',  # Adjust as necessary
                        value=temperature,  # You can save moisture in another instance if needed
                        timestamp=timestamp
                    )
                    sensor_data.save()

                    # Send data to WebSocket group
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "sensor_data",
                        {
                            "type": "send_sensor_data",
                            "data": {
                                "timestamp": sensor_data.timestamp,
                                "temperature": sensor_data.value,  # or save moisture if applicable
                                "moisture": moisture
                            }
                        }
                    )

                    return JsonResponse({"status": "success"})
                else:
                    return JsonResponse({"status": "failed", "error": "Required fields not found in response"})
            else:
                return JsonResponse({"status": "failed",
                                     "error": f"Error fetching data from ThingSpeak: {response.status_code} - {response.text}"},
                                    status=500)
        except Exception as e:
            return JsonResponse({"status": "failed", "error": f"Error: {e}"}, status=500)

    return JsonResponse({"status": "failed", "error": "Invalid request method"}, status=400)


class SensorDataView(View):
    def post(self, request):
        data = json.loads(request.body)

        # Create a new SensorData instance
        sensor_data = SensorData(
            user=data['user'],
            sensorName=data['sensorName'],
            location=data['location'],
            physicalQuantity=data['physicalQuantity'],
            value=data['value'],
            timestamp=data['timestamp'] or timezone.now().isoformat()  # Default to now if not provided
        )
        sensor_data.save()

        # Broadcast the new sensor data to WebSocket clients
        self.broadcast_sensor_data(sensor_data)

        return JsonResponse({'status': 'success', 'data': data})

    def broadcast_sensor_data(self, sensor_data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'sensor_data_group',  # Use a specific group name for your WebSocket group
            {
                'type': 'sensor_data_update',
                'sensor_data': {
                    'user': sensor_data.user,
                    'sensorName': sensor_data.sensorName,
                    'location': sensor_data.location,
                    'physicalQuantity': sensor_data.physicalQuantity,
                    'value': sensor_data.value,
                    'timestamp': sensor_data.timestamp,
                }
            }
        )


@csrf_exempt
def store_sensor_data(request):
    if request.method == 'POST':
        try:
            # Load JSON data from request body
            data = json.loads(request.body)

            # Create a new SensorData object and save to MongoDB
            sensor_data = SensorData(
                user=data['user'],
                sensorName=data['sensorName'],
                location=data['location'],
                physicalQuantity=data['physicalQuantity'],
                value=data['value'],
                timestamp=data.get('timestamp', timezone.now().isoformat())  # Default to now if not provided
            )
            sensor_data.save()

            return JsonResponse({"message": "Data saved successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


def get_all_sensor_data(request):
    if request.method == 'GET':
        try:
            # Fetch all sensor data from MongoDB
            sensor_data_list = SensorData.get_all_data()

            # Create a list of dictionaries to hold the data
            sensor_data_response = [
                {
                    "user": data['user'],
                    "sensorName": data['sensorName'],
                    "location": data['location'],
                    "physicalQuantity": data['physicalQuantity'],
                    "value": data['value'],
                    "timestamp": data['timestamp']
                } for data in sensor_data_list
            ]

            return JsonResponse(sensor_data_response, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)
