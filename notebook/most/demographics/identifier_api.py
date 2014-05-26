#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

HOST_ADDRESS = 'http://127.0.0.1:8000'
IDENTIFIER_DATA = {
    'type': 'business',
    'domain': 'hospital_1',
    'identifier': '0123456789'
}


def call_identifier_new():
    """ call /demographics/identifier/new/

        method: 'POST'
        data: '{'type': String or None,'domain': String or None,'identifier': String}'
    """
    print 'In call_identifier_new method'
    client = requests.Session()
    # make a request to the server to obtain csrf token
    pre_request = client.get(HOST_ADDRESS)
    csrf_token = pre_request.cookies['csrftoken']
    # post json data to the server. Make sure to set properly "headers" attribute!
    response = client.post('%s/demographics/identifier/new/' % HOST_ADDRESS,
                           data=json.dumps(IDENTIFIER_DATA),
                           headers={
                               'X-CSRFToken': csrf_token,
                               'content-type': 'application/json',
                               'referer': '%s/demographics/identifier/new/' % HOST_ADDRESS,
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


def call_identifier_get():
    """ call /demographics/identifier/get/

        method: 'GET'
        param: 'query_string': String
    """
    print 'In call_identifier_get method'
    # get an identifier from the server
    response = requests.get('%s/demographics/identifier/get/' % HOST_ADDRESS, params={'query_string': '0123456789'})
    response.encoding = 'ISO-8859-15'
    response_dict = response.json()
    print u'JSON response: %s' % response_dict
    if response_dict['success']:
        print u'identifiers data:\n%s' % json.dumps(response_dict['data'], indent=4, separators=(',', ': '))
    else:
        print response_dict['errors']


if __name__ == "__main__":
    print 'Identifier API'
    print 100 * '*'
    call_identifier_new()
    print 100 * '*'
    call_identifier_get()
    print 100 * '*', '\n'
