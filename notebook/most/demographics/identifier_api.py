# -*- coding: utf-8 -*-
from helper import *


HOST_ADDRESS = 'http://127.0.0.1:8000'
IDENTIFIER_DATA = {
    'type': 'business',
    'domain': 'hospital_1',
    'identifier': '0123456789'
}


identifier = compose_post_request(HOST_ADDRESS, '/demographics/identifier/new/', IDENTIFIER_DATA)
print_response_data('identifier', identifier)
identifier = compose_get_request(HOST_ADDRESS, '/demographics/identifier/get/', '01234')
print_response_data('identifier', identifier)
