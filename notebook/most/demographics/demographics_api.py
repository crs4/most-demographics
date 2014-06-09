#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import city_api, identifier_api, patient_api

HOST_ADDRESS = 'http://127.0.0.1:8000'
IDENTIFIER_DATA = {
    'type': 'business',
    'domain': 'hospital_1',
    'identifier': '0123456789'
}
CITY_DATA = {
    'name': 'Milano',
    'province': 'MI',
    'state': 'Italia',
    'code': '20100'
}
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
APIs = {
    'create_identifier': '/demographics/identifier/new/',
    'get_identifier': '/demographics/identifier/get/',
    'create_city': '/demographics/city/new/',
    'get_city': '/demographics/city/get/',
    'create_patient': '/demographics/patient/new/',
    'get_patient': '/demographics/patient/get/'
}


def print_response_data(class_name, dictionary):
    print u'JSON response: %s\n' % dictionary
    if dictionary['success']:
        # dump dictionary to print human readable data
        print u'%s data:\n%s' % (class_name, json.dumps(dictionary['data'], sort_keys=True, indent=4,
                                                        separators=(',', ': ')))
    else:
        print dictionary['errors']


def compose_post_request(api, data):
    print 'Calling %s\n' % api
    response = requests.post('%s%s' % (HOST_ADDRESS, api), data=json.dumps(data),
                             headers={'content-type': 'application/json', 'accept': '*/*',
                                      'X-Requested-With': 'XMLHttpRequest'})
    print response.text
    return response.json()


def compose_get_request(api, params):
    print 'Calling %s\n' % api
    response = requests.get('%s%s' % (HOST_ADDRESS, api), params={'query_string': params})
    return response.json()


def create_patient_from_scratch():
    try:
        identifier = compose_post_request(APIs['create_identifier'], IDENTIFIER_DATA)
        print_response_data('identifier', identifier)
        print 120 * '-', '\n'
        city = compose_post_request(APIs['create_city'], CITY_DATA)
        print_response_data('city', city)
        print 120 * '-', '\n'
        patient = compose_post_request(APIs['create_patient'], PATIENT_DATA)
        print_response_data('patient', patient)
        print 120 * '-', '\n'
        search_patients = compose_get_request(APIs['get_patient'], 'rossi ma')
        print_response_data('patient', search_patients)
        print 120 * '-', '\n'
    except Exception, e:
        print e


if __name__ == "__main__":
    create_patient_from_scratch()

