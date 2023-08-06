import requests
from get_device_id import get_device_id
from refresh_token import refresh_token
from get_token import get_token
import os

def get_game_state(api_key=None, device_id=None):
    DEVICE_ID = get_device_id() if device_id is None else device_id
    API_KEY = get_token() if api_key is None else api_key
    url = f'http://api.illuvium-game.io/gamedata/api/zero/gamestate?active_device_id={DEVICE_ID}'

    response = requests.get(url, headers={'Authorization':
                            'Bearer ' + API_KEY})
    if response.status_code == 401:
        print('Token expired, refreshing...')
        API_KEY = refresh_token()
        response = requests.get(url, headers={'Authorization':
                                              'Bearer ' + API_KEY})
        os.environ['API_KEY'] = API_KEY
    
    response_json = response.json()
    plots = response_json['data']
    return plots
