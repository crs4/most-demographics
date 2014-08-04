# -*- coding: utf-8 -*-
#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

from django.test import TestCase
from django.core.urlresolvers import reverse
from demographics.models import Patient, City, Identifier
import json
from django.db.models import Q


def create_identifier(identifier, type=None, domain=None):
    """
    Create an identifier with given arguments
    """
    identifier, created = Identifier.objects.get_or_create(type=type, domain=domain, identifier=identifier)
    return identifier


def get_identifier_by_query_string(query_string):
    """
    Get an identifier by given query string
    """
    query_set = (Q())
    query_list = [query for query in query_string.split(' ') if query]
    for query in query_list:
        query_set = query_set & (
            Q(identifier__icontains=query) |
            Q(type__icontains=query) |
            Q(domain__icontains=query)
        )
    identifiers = []
    for identifier in Identifier.objects.filter(query_set):
        identifiers.append(identifier.to_dictionary())
    return identifiers


def edit_identifier(identifier_id, identifier=None, type=None, domain=None):
    """
    Edit a identifier with given arguments
    """
    identifiers = Identifier.objects.filter(pk=identifier_id)
    identifiers.update(
        identifier=identifier,
        type=type,
        domain=domain
    )
    identifier = identifiers[0]
    identifier.save()
    return identifier


def create_city(name, state, province=None, code=None):
    """
    Create a city with given arguments
    """
    city, created = City.objects.get_or_create(name=name, province=province, state=state, code=code)
    return city


def get_city_by_query_string(query_string):
    """
    Get a city by given query string
    """
    query_set = (Q())
    query_list = [query for query in query_string.split(' ') if query]
    for query in query_list:
        query_set = query_set & (
            Q(name__icontains=query) |
            Q(state__icontains=query) |
            Q(province__icontains=query) |
            Q(code__icontains=query)
        )
    cities = []
    for city in City.objects.filter(query_set):
        cities.append(city.to_dictionary())
    return cities


def edit_city(city_id, name=None, state=None, province=None, code=None):
    """
    Edit a city with given arguments
    """
    cities = City.objects.filter(pk=city_id)
    cities.update(
        name=name,
        state=state,
        province=province,
        code=code
    )
    city = cities[0]
    city.save()
    return city


def create_patient(first_name, last_name, gender, birth_date, birth_place, account_number=None, address=None, city=None,
                   phone=None, mobile=None, email=None, certified_email=None, *other_ids):
    """
    Create a patient with given arguments
    """
    patient, created = Patient.objects.get_or_create(
        account_number=account_number,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birth_date=birth_date,
        birth_place=birth_place,
        address=address,
        city=city,
        phone=phone,
        mobile=mobile,
        email=email,
        certified_email=certified_email
    )
    for identifier_id in other_ids:
        try:
            identifier = Identifier.objects.get(pk=identifier_id)
            patient.add(identifier)
        except:
            continue
    patient.save()
    return patient


def get_patient_by_query_string(query_string):
    """
    Get a patient by given query string
    """
    query_set = (Q())
    query_list = [query for query in query_string.split(' ') if query]
    for query in query_list:
        query_set = query_set & (
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(account_number__icontains=query)
        )
    patients = []
    for patient in Patient.objects.filter(query_set):
        patients.append(patient.to_dictionary())
    return patients


def edit_patient(patient_id, first_name=None, last_name=None, gender=None, birth_date=None, birth_place=None, account_number=None, address=None, city=None,
                   phone=None, mobile=None, email=None, certified_email=None, *other_ids):
    """
    Edit a patient with given arguments
    """
    patients = Patient.objects.filter(pk=patient_id)
    patients.update(
        account_number=account_number,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birth_date=birth_date,
        birth_place=birth_place,
        address=address,
        city=city,
        phone=phone,
        mobile=mobile,
        email=email,
        certified_email=certified_email
    )
    patient = patients[0]
    for identifier_id in other_ids:
        try:
            identifier = Identifier.objects.get(pk=identifier_id)
            patient.add(identifier)
        except:
            continue
    patient.save()
    return patient


class PatientAPITest(TestCase):
    def setUp(self):
        self.birth_place = create_city(name='Rome', state='Italy', province='RM', code='00199')
        self.patient = create_patient(
            account_number='0123456789012345',
            first_name='Test1',
            last_name='Test1',
            gender='M',
            birth_date='1970-01-01',
            birth_place=self.birth_place
        )
        self.patient_clone = create_patient(
            account_number='0123456789012345',
            first_name='Test1',
            last_name='Test1',
            gender='M',
            birth_date='1970-01-01',
            birth_place=self.birth_place
        )

    def test_patient_new(self):
        patient_data = {
            'first_name': 'Name1',
            'last_name': 'LastName1',
            'gender': 'M',
            'birth_date': '1980-01-01',
            'birth_place': self.birth_place.id
        }
        response = self.client.post('/demographics/patient/new/', data=json.dumps(patient_data),
                                    content_type='application/json; charset=utf8',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        patient = create_patient(
            first_name=patient_data['first_name'],
            last_name=patient_data['last_name'],
            gender=patient_data['gender'],
            birth_date=patient_data['birth_date'],
            birth_place=self.birth_place
        )
        self.assertEqual(patient.to_dictionary(), json.loads(response.content)['data'], 'test_patient_new --> KO')

    def test_patient_get(self):
        query_string = 'Test'
        patient = get_patient_by_query_string(query_string)
        response = self.client.get('/demographics/patient/get/', data={'query_string': query_string})
        self.assertEqual(patient, json.loads(response.content)['data'], 'test_patient_get --> KO')

    def test_patient_edit(self):
        patient_data = {
            'first_name': 'Name1bis',
            'last_name': 'LastName1bis',
            'gender': 'M',
            'birth_date': '1980-01-01',
            'birth_place': self.birth_place.id
        }
        response = self.client.post('/demographics/patient/%s/edit/' % self.patient.pk, data=json.dumps(patient_data),
                                    content_type='application/json; charset=utf8',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_dictionary = json.loads(response.content)['data']
        response_dictionary.pop('id')
        patient = edit_patient(
            self.patient_clone.pk,
            first_name=patient_data['first_name'],
            last_name=patient_data['last_name'],
            gender=patient_data['gender'],
            birth_date=patient_data['birth_date'],
            birth_place=self.birth_place
        )
        patient_dictionary = patient.to_dictionary()
        patient_dictionary.pop('id')
        self.assertEqual(patient_dictionary, response_dictionary, 'test_patient_edit --> KO')

    def test_patient_deactivate(self):
        pass

    def test_patient_activate(self):
        pass

    def test_patient_add_identifier(self):
        pass

    def test_patient_remove_id(self):
        pass

    def patient_set_birth_place(self):
        pass

    def patient_set_city(self):
        pass


class CityAPITest(TestCase):
    def setUp(self):
        self.city = create_city(name='CityA', province='PA', state='StateA', code='XXXXX')
        self.city_clone = create_city(name='CityA', province='PA', state='StateA', code='YYYYY')

    def test_city_new(self):
        city_data = {
            'name': 'City1',
            'province': 'P1',
            'state': 'State1',
            'code': '12345'
        }
        response = self.client.post('/demographics/city/new/', data=json.dumps(city_data),
                                    content_type='application/json; charset=utf8',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        city = create_city(
            name=city_data['name'],
            province=city_data['province'],
            state=city_data['state'],
            code=city_data['code']
        )
        self.assertEqual(city.to_dictionary(), json.loads(response.content)['data'], 'test_city_new --> KO')

    def test_city_get(self):
        query_string = 'Test'
        city = get_city_by_query_string(query_string)
        response = self.client.get('/demographics/city/get/', data={'query_string': query_string})
        self.assertEqual(city, json.loads(response.content)['data'], 'test_city_get --> KO')

    # def test_city_edit(self):
    #     city_data = {
    #         'name': 'City1bis',
    #         'province': 'P1',
    #         'state': 'State1bis',
    #         'code': self.city.code
    #     }
    #     response = self.client.post('/demographics/city/%s/edit/' % self.city.pk, data=json.dumps(city_data),
    #                                 content_type='application/json; charset=utf8',
    #                                 HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #     print response.content
    #     response_dictionary = json.loads(response.content)['data']
    #     response_dictionary.pop('id', 'code')
    #     city = edit_city(
    #         self.city_clone.pk,
    #         name=city_data['name'],
    #         province=city_data['province'],
    #         state=city_data['state'],
    #         code=self.city_clone.code
    #     )
    #     city_dictionary = city.to_dictionary()
    #     city_dictionary.pop('id', 'code')
    #     self.assertEqual(city_dictionary, response_dictionary, 'test_city_edit --> KO')


class IdentifierAPITest(TestCase):
    def setUp(self):
        self.identifier = create_identifier(
            identifier='0123456789012345',
            type='Test1',
            domain='Test1'
        )
        self.identifier_clone = create_identifier(
            identifier='0123456789012345',
            type='Test1',
            domain='Test1'
        )

    def test_identifier_new(self):
        identifier_data = {
            'identifier': 'Identifier1',
            'type': 'Type1',
            'domain': 'Domain1'
        }
        response = self.client.post('/demographics/identifier/new/', data=json.dumps(identifier_data),
                                    content_type='application/json; charset=utf8',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        identifier = create_identifier(
            identifier=identifier_data['identifier'],
            type=identifier_data['type'],
            domain=identifier_data['domain']
        )
        self.assertEqual(identifier.to_dictionary(), json.loads(response.content)['data'], 'test_identifier_new --> KO')

    def test_identifier_get(self):
        query_string = 'Identifier'
        identifier = get_identifier_by_query_string(query_string)
        response = self.client.get('/demographics/identifier/get/', data={'query_string': query_string})
        self.assertEqual(identifier, json.loads(response.content)['data'], 'test_identifier_get --> KO')

    def test_identifier_edit(self):
        identifier_data = {
            'identifier': '0123456789012345',
            'type': 'Test1bis',
            'domain': 'Test1bis'
        }
        response = self.client.post('/demographics/identifier/%s/edit/' % self.identifier.pk, data=json.dumps(identifier_data),
                                    content_type='application/json; charset=utf8',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_dictionary = json.loads(response.content)['data']
        response_dictionary.pop('id')
        identifier = edit_identifier(
            self.identifier_clone.pk,
            identifier=identifier_data['identifier'],
            type=identifier_data['type'],
            domain=identifier_data['domain']
        )
        identifier_dictionary = identifier.to_dictionary()
        identifier_dictionary.pop('id')
        self.assertEqual(identifier_dictionary, response_dictionary, 'test_identifier_edit --> KO')