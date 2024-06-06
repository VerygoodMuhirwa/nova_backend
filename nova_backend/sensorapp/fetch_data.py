import time
import requests
import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import pytz

def reverse_moisture_reading(moisture):
    print(moisture)
    return 1024 - moisture

def fetch_data_from_thingspeak(channel_id, read_api_key, interval=10):
    url = f'https://api.thingspeak.com/channels/{channel_id}/feeds/last.json?api_key={read_api_key}'
    channel_layer = get_channel_layer()

    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'field1' in data and 'field2' in data:
                    temperature = data['field1']
                    moisture = data['field2']

                    if moisture is not None:
                        reversed_moisture = reverse_moisture_reading(int(moisture))
                    else:
                        reversed_moisture = None

                    receive_time = datetime.datetime.now(pytz.utc)

                    async_to_sync(channel_layer.group_send)(
                        "sensor_data",
                        {
                            "type": "send_sensor_data",
                            "data": {
                                "temperature": temperature,
                                "moisture": reversed_moisture,
                                "time": receive_time.isoformat()
                            }
                        }
                    )
                    print(f"Temperature: {temperature}, Moisture: {reversed_moisture}, Time: {receive_time.isoformat()}")
                else:
                    print("Error: Required fields not found in response")
            else:
                print(f"Error fetching data from ThingSpeak: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error fetching data from ThingSpeak: {e}")
        time.sleep(interval)
