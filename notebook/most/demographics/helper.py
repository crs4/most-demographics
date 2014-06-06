#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json


def print_response_data(class_name, dictionary):
    print u'JSON response: %s\n' % dictionary
    if dictionary['success']:
        # dump dictionary to print human readable data
        print u'%s data:\n%s' % (class_name, json.dumps(dictionary['data'], sort_keys=True, indent=4,
                                                        separators=(',', ': ')))
    else:
        print dictionary['errors']


def compose_post_request(host, api, data):
    print 'Calling %s\n' % api
    response = requests.post('%s%s' % (host, api), data=json.dumps(data),
                             headers={'content-type': 'application/json', 'accept': '*/*',
                                      'X-Requested-With': 'XMLHttpRequest'})
    # print response.text
    return response.json()


def compose_get_request(host, api, params):
    print 'Calling %s\n' % api
    response = requests.get('%s%s' % (host, api), params={'query_string': params})
    return response.json()
