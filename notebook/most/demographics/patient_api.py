# -*- coding: utf-8 -*-
from helper import *


HOST_ADDRESS = 'http://127.0.0.1:8000'
PATIENT_DATA = {
    'account_number': 'RSSMRA80H51B354M',
    'first_name': 'Maria',
    'last_name': 'Rossi',
    'other_ids': [1],
    'gender': 'F',
    'birth_date': '1980-06-11',
    'birth_place': 1,
    'address': 'Via Cagliari 4',
    'city': 4,
    'active': True
}


patient = compose_post_request(HOST_ADDRESS, '/demographics/patient/new/', PATIENT_DATA)
print_response_data('patient', patient)
patient = compose_get_request(HOST_ADDRESS, '/demographics/patient/get/', 'RSS')
print_response_data('patient', patient)