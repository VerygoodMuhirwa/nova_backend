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
def store_sensor_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)

            # Create a new SensorData object and save to MongoDB
            sensor_data = SensorData(
                user=data['user'],
                sensorId=data['sensorId'],
                sensorName=data['sensorName'],
                location=data['location'],
                physicalQuantity=data['physicalQuantity'],
                temperatureValue=data['temperatureValue'],
                moistureValue=data["moistureValue"],
                timestamp=data.get('timestamp', timezone.now().isoformat())  # Default to now if not provided
            )
            sensor_data.save()

            sensor_data_list = SensorData.get_all_data()

            formatted_data = format_sensor_data(sensor_data_list)

            print("Broadcasting the following sensor data:", formatted_data)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'sensor_data_group',  # Replace with your WebSocket group name
                {
                    'type': 'sensor_data_update',
                    'sensor_data': formatted_data
                }
            )

            # Return success response
            return JsonResponse({"message": "Data saved and broadcasted successfully"}, status=201)

        except Exception as e:
            # Handle any errors and return a failure response
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)



def format_sensor_data(sensor_data_list):
    """
    Format the sensor data list into the desired format for WebSocket broadcast.
    """
    grouped_sensor_data = {}
    for data in sensor_data_list:
        sensor_name = data['sensorName']
        sensor_id = data['sensorId']

        if sensor_name not in grouped_sensor_data:
            grouped_sensor_data[sensor_name] = []

        if sensor_name.lower() == 'Humidity_sensor':
            humidity_group = next((group for group in grouped_sensor_data[sensor_name] if group['sensorId'] == sensor_id), None)
            if humidity_group is None:
                humidity_group = {
                    "sensorId": sensor_id,
                    "data": []
                }
                grouped_sensor_data[sensor_name].append(humidity_group)

            humidity_group['data'].append({
                "user": data['user'],
                "location": data['location'],
                "physicalQuantity": data['physicalQuantity'],
                "temperatureValue": data['temperatureValue'],
                "moistureValue": data["moistureValue"],
                "timestamp": data['timestamp']
            })
        else:
            grouped_sensor_data[sensor_name].append({
                "user": data['user'],
                "location": data['location'],
                "physicalQuantity": data['physicalQuantity'],
                "temperatureValue": data['temperatureValue'],
                "moistureValue": data["moistureValue"],
                "timestamp": data['timestamp']
            })

    return grouped_sensor_data



def get_all_sensor_data(request):
    if request.method == 'GET':
        try:
            sensor_data_list = SensorData.get_all_data()

            grouped_sensor_data = {}

            for data in sensor_data_list:
                sensor_name = data['sensorName']
                sensor_id = data.get('sensorId')

                # Initialize the list for this sensor name if it doesn't exist
                if sensor_name not in grouped_sensor_data:
                    grouped_sensor_data[sensor_name] = []

                # Handle humidity sensor differently by grouping by sensor ID
                if sensor_name.lower() == 'Humidity_sensor':
                    # Initialize the list for this sensor ID if it doesn't exist
                    humidity_group = next((group for group in grouped_sensor_data[sensor_name] if group['sensorId'] == sensor_id), None)
                    if humidity_group is None:
                        humidity_group = {
                            "sensorId": sensor_id,
                            "data": []
                        }
                        grouped_sensor_data[sensor_name].append(humidity_group)

                    # Append the data to the corresponding sensor ID group
                    humidity_group['data'].append({
                        "user": data['user'],
                        "location": data['location'],
                        "physicalQuantity": data['physicalQuantity'],
                        "temperatureValue": data['temperatureValue'],
                        "moistureValue": data["moistureValue"],
                        "timestamp": data['timestamp']
                    })
                else:
                    # For other sensor types, append the data directly under the sensor name
                    grouped_sensor_data[sensor_name].append({
                        "user": data['user'],
                        "location": data['location'],
                        "physicalQuantity": data['physicalQuantity'],
                        "temperatureValue": data['temperatureValue'],
                        "moistureValue": data["moistureValue"],
                        "timestamp": data['timestamp']
                    })

            return JsonResponse(grouped_sensor_data, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)



