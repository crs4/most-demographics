# -*- coding: utf-8 -*-
from helper import *


HOST_ADDRESS = 'http://127.0.0.1:8000'
CITY_DATA = {
    'name': 'Milano',
    'province': 'MI',
    'state': 'Italia',
    'code': '20100'
}


city = compose_post_request(HOST_ADDRESS, '/demographics/city/new/', CITY_DATA)
print_response_data('city', city)
city = compose_get_request(HOST_ADDRESS, '/demographics/city/get/', 'Mi')
print_response_data('city', city)