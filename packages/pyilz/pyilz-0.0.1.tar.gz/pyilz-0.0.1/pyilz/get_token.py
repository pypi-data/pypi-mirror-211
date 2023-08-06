import os
from refresh_token import refresh_token


def get_token(ref_token=None):
    API_KEY = os.getenv('API_KEY')
    if API_KEY:
        return API_KEY
    else:
        print('No token found, refreshing...')
        API_KEY = refresh_token(ref_token)
        os.environ['API_KEY'] = API_KEY
    return API_KEY
