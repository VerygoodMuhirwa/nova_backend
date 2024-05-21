import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import datetime


@csrf_exempt
def fetch_and_receive_data(request):
    if request.method == "POST":
        try:
            # Fetch data from ThingSpeak
            channel_id = '2511877'
            read_api_key = 'YX33ECEWQJ1PXWKJ'
            url = f'https://api.thingspeak.com/channels/{channel_id}/feeds/last.json?api_key={read_api_key}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if 'field1' in data and 'field2' in data:
                    temperature = float(data['field1'])
                    moisture = float(data['field2'])
                    timestamp = datetime.datetime.now().isoformat()

                    # Save data to the database
                    sensor_data = SensorData.objects.create(
                        temperature=temperature,
                        moisture=moisture,
                        timestamp=timestamp
                    )

                    # Send data to WebSocket group
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "sensor_data",
                        {
                            "type": "send_sensor_data",
                            "data": {
                                "timestamp": sensor_data.timestamp.isoformat(),
                                "temperature": sensor_data.temperature,
                                "moisture": sensor_data.moisture
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
