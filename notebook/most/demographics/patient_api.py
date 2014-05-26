#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

HOST_ADDRESS = 'http://127.0.0.1:8000'
PATIENT_DATA = {
    'account_number': 'RSSMRA80H51B354M',
    'first_name': 'Maria',
    'last_name': 'Rossi',
    'other_ids': [1],
    'gender': 'F',
    'birth_date': '1980-06-11',
    'birth_place': 1,
    'address': 'Via Muravera 4',
    'city': 4,
    'active': True
}


def call_patient_new():
    """ call /demographics/patient/new/

        method: 'POST'
        data: {'account_number': String or None, 'first_name': String, 'last_name': String,
               'other_ids': Array of Int or None, 'gender': 'M' | 'F', 'birth_date': Date, 'birth_place': Int,
               'address': String or None, 'city': Int or None, 'phone': String or None, 'mobile': String or None,
               'email': String or None, 'certified_email': String or None, 'active': True | False}
    """
    print 'In call_patient_new method'
    client = requests.Session()
    # make a request to the server to obtain csrf token
    pre_request = client.get(HOST_ADDRESS)
    csrf_token = pre_request.cookies['csrftoken']
    # post json data to the server. Make sure to set properly "headers" attribute!
    response = client.post('%s/demographics/patient/new/' % HOST_ADDRESS,
                           data=json.dumps(PATIENT_DATA),
                           headers={
                               'X-CSRFToken': csrf_token,
                               'content-type': 'application/json',
                               'referer': '%s/demographics/patient/new/' % HOST_ADDRESS,
                               'accept': '*/*',
                               'X-Requested-With': 'XMLHttpRequest'
                           })
    response.encoding = 'ISO-8859-15'
    response_dict = response.json()
    print u'JSON response: %s' % response_dict
    if response_dict['success']:
        print u'identifier data:\n%s' % json.dumps(response_dict['data'], indent=4, separators=(',', ': '))
    else:
        print response_dict['errors']


def call_patient_get():
    """ call /demographics/patient/get/

        method: 'GET'
        param: 'query_string': String
    """
    print 'In call_patient_get method'
    # get an patient from the server
    response = requests.get('%s/demographics/patient/get/' % HOST_ADDRESS, params={'query_string': 'rss'})
    response.encoding = 'ISO-8859-15'
    response_dict = response.json()
    print u'JSON response: %s' % response_dict
    if response_dict['success']:
        print u'identifiers data:\n%s' % json.dumps(response_dict['data'], indent=4, separators=(',', ': '))
    else:
        print response_dict['errors']


if __name__ == "__main__":
    print 'Patient API'
    print 100 * '*'
    call_patient_new()
    print 100 * '*'
    call_patient_get()
    print 100 * '*', '\n'
