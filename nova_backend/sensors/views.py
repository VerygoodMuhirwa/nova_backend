
import time
from django.views.decorators.csrf import csrf_protect
import requests
import datetime
import pusher
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user import views
def fetch_data_from_thingspeak(channel_id, read_api_key, interval=10):
    url = f'https://api.thingspeak.com/channels/{channel_id}/feeds/last.json?api_key={read_api_key}'
    pusher_client = pusher.Pusher(app_id='1790247',key='b474acc965ca822765e5', secret='bf7388a5ea126e94ce2e',cluster='eu', ssl=True)
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'field1' in data and 'field2' in data:  
                    temperature = data['field1']
                    moisture = data['field2']
                    receive_time = datetime.datetime.now().isoformat()
                    pusher_client.trigger('nova_data', 'sensor_data_event', {'temperature': temperature,  "moisture":moisture,  "time": receive_time})
                    print(f"Temperature: {temperature}, Moisture: {moisture}, Time: {receive_time}")
                    
                else:
                    print("Error: Required fields not found in response")
            else:
                print(f"Error fetching data from ThingSpeak: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error fetching data from ThingSpeak: {e}")
        time.sleep(interval)
    

@csrf_protect
@api_view(["GET"])
@views.authenticate_user
def fetch_thingspeak_data_view(request):
    if request.user_id:
        channel_id = '2511877'
        read_api_key = 'YX33ECEWQJ1PXWKJ'
        fetch_data_from_thingspeak(channel_id, read_api_key)
    else:
        return Response("Not authorized", status=403);
    
    
    