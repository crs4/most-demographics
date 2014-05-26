#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

HOST_ADDRESS = 'http://127.0.0.1:8000'
CITY_DATA = {
    'name': 'Milano',
    'province': 'MI',
    'state': 'Italia',
    'code': '20100'
}


def call_city_new():
    """ call /demographics/city/new/

        method: 'POST'
        data: '{'name': String,'province': String or None,'state': String, code: String or None}'
    """
    print 'In call_city_new method'
    client = requests.Session()
    # make a request to the server to obtain csrf token
    pre_request = client.get(HOST_ADDRESS)
    csrf_token = pre_request.cookies['csrftoken']
    # post json data to the server. Make sure to set properly "headers" attribute!
    response = client.post('%s/demographics/city/new/' % HOST_ADDRESS,
                           data=json.dumps(CITY_DATA),
                           headers={
                               'X-CSRFToken': csrf_token,
                               'content-type': 'application/json',
                               'referer': '%s/demographics/city/new/' % HOST_ADDRESS,
                               'accept': '*/*',
                               'X-Requested-With': 'XMLHttpRequest'
                           })
    response.encoding = 'ISO-8859-15'
    response_dict = response.json()
    print u'JSON response: %s' % response_dict
    if response_dict['success']:
        print u'city data:\n%s' % json.dumps(response_dict['data'], sort_keys=True, indent=4, separators=(',', ': '))
    else:
        print response_dict['errors']

def call_city_get():
    """ call /demographics/city/get/

        method: 'GET'
        param: 'query_string': String
    """
    print 'In call_city_get method'
    # get a city from the server
    response = requests.get('%s/demographics/city/get/' % HOST_ADDRESS, params={'query_string': 'milan'})
    response.encoding = 'ISO-8859-15'
    response_dict = response.json()
    print u'JSON response: %s' % response_dict
    if response_dict['success']:
        print u'cities data:\n%s' % json.dumps(response_dict['data'], sort_keys=True, indent=4, separators=(',', ': '))
    else:
        print response_dict['errors']


if __name__ == "__main__":
    print 'City API'
    print 100 * '*'
    call_city_new()
    print 100 * '*'
    call_city_get()
    print 100 * '*', '\n'
