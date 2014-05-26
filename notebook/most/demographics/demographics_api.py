#!/usr/bin/env python
# -*- coding: utf-8 -*-

import city_api, identifier_api, patient_api


if __name__ == "__main__":
    print 'Identifier API'
    print 120 * '-'
    identifier_api.call_identifier_new()
    print 120 * '-'
    identifier_api.call_identifier_get()
    print 120 * '-', '\n'
    print 'City API'
    print 120 * '-'
    city_api.call_city_new()
    print 120 * '-'
    city_api.call_city_get()
    print 120 * '-', '\n'
    print 'Patient API'
    print 120 * '-'
    patient_api.call_patient_new()
    print 120 * '-'
    patient_api.call_patient_get()
    print 120 * '-', '\n'
