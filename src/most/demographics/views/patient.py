# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils.translation import ugettext as _
import json
from datetime import date, datetime
from django.db.models import Q
from ..models import Patient, City, Identifier
from ..forms import PatientForm
from . import SUCCESS_KEY, MESSAGE_KEY, ERRORS_KEY, DATA_KEY, TOTAL_KEY


@csrf_exempt
@require_POST
def new(request):
    """Add new patient, assuming only POST requests containing JSON data.

    POST JSON:
        {'account_number': String or None,
         'first_name': String,
         'last_name': String,
         'other_ids': Array of Int or None,
         'gender': 'M' | 'F',
         'birth_date': Date,
         'birth_place': Int,
         'address': String or None,
         'city': Int or None,
         'phone': String or None,
         'mobile': String or None,
         'email': String or None,
         'certified_email': String or None,
         'active': True | False}
    """
    result = {}
    errors = ''
    if request.is_ajax():
        if request.method == 'POST':
            # check required fields: first_name, last_name, gender, birth_date, birth_place
            try:
                patient_data = json.loads(request.body)
                mandatory_fields_checked = True
                for field in Patient.MANDATORY_FIELDS:
                    try:
                        if field not in patient_data:
                            errors += _('Field %s is mandatory\n' % field)
                            mandatory_fields_checked = False
                    except Exception, e:
                        errors += u'%s\n' % e
                if not mandatory_fields_checked:
                    result[ERRORS_KEY] = errors
                    result[SUCCESS_KEY] = False
                else:
                    try:
                        if 'other_ids' in patient_data:
                            other_ids = patient_data.pop('other_ids')
                        else:
                            other_ids = None
                        patient_data['birth_place'] = City.objects.get(pk=patient_data['birth_place'])
                        if 'city' in patient_data:
                            patient_data['city'] = City.objects.get(pk=patient_data['city'])
                        patient = Patient(**patient_data)
                        patient.save()
                        if other_ids:
                            for identifier in other_ids:
                                patient.other_ids.add(identifier)
                            patient.save()
                        result[SUCCESS_KEY] = True
                        result[MESSAGE_KEY] = _('Patient %s successfully created' % patient.pk)
                        result[DATA_KEY] = patient.to_dictionary()
                    except Exception, e:
                        errors += u'%s\n' % e
                        result[ERRORS_KEY] = errors
                        result[SUCCESS_KEY] = False
            except Exception, e:
                errors += u'%s\n' % e
                result[ERRORS_KEY] = errors
                result[SUCCESS_KEY] = False
        else:
            result[ERRORS_KEY] = _('POST method required.\n')
            result[SUCCESS_KEY] = False
    else:
        result[ERRORS_KEY] = _('Ajax data required.\n')
        result[SUCCESS_KEY] = False
    return HttpResponse(json.dumps(result), content_type='application/json; charset=utf8')


@require_GET
def get(request):
    """Get a patient by a query string"""
    result = {}
    errors = ''
    query_set = (Q())
    if request.method == 'GET':
        try:
            query_string = request.GET['query_string']
            query_list = [query for query in query_string.split(' ') if query]
            for query in query_list:
                query_set = query_set & (
                    Q(last_name__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(account_number__icontains=query)
                )
            patients = Patient.objects.filter(query_set)
            result[DATA_KEY] = []
            for patient in patients:
                result[DATA_KEY].append(patient.to_dictionary())
            if result[DATA_KEY]:
                result[MESSAGE_KEY] = _('%(patients_count)s patients found with query string: \'%(query_string)s\'' %
                                        {'patients_count': patients.count(), 'query_string': query_string})
                result[TOTAL_KEY] = patients.count()
            else:
                result[MESSAGE_KEY] = _('No patients found for query string: \'%s\'' % query_string)
            result[SUCCESS_KEY] = True
        except Exception, e:
            errors += u'%s\n' % e
            result[ERRORS_KEY] = errors
            result[SUCCESS_KEY] = False
    else:
        result[ERRORS_KEY] = _('GET method required.\n')
        result[SUCCESS_KEY] = False
    return HttpResponse(json.dumps(result), content_type='application/json; charset=utf8')


@csrf_exempt
@require_POST
def edit(request, patient_id):
    """Edit patient data, assuming only POST requests containing JSON data.

    POST JSON:
        {'id': String,
         'account_number': String or None,
         'first_name': String,
         'last_name': String,
         'other_ids': Array of Int or None,
         'gender': 'M' | 'F',
         'birth_date': Date,
         'birth_place': Int,
         'address': String or None,
         'city': Int or None,
         'phone': String or None,
         'mobile': String or None,
         'email': String or None,
         'certified_email': String or None,
         'active': True | False}
    """
    result = {}
    errors = ''
    if request.is_ajax():
        if request.method == 'POST':
            # check required fields: first_name, last_name, gender, birth_date, birth_place
            try:
                patient_data = json.loads(request.body)
                mandatory_fields_checked = True
                for field in Patient.MANDATORY_FIELDS:
                    try:
                        if field not in patient_data:
                            errors += _('Field %s is mandatory\n' % field)
                            mandatory_fields_checked = False
                    except Exception, e:
                        errors += u'%s\n' % e
                if not mandatory_fields_checked:
                    result[ERRORS_KEY] = errors
                    result[SUCCESS_KEY] = False
                else:
                    try:
                        if 'other_ids' in patient_data:
                            other_ids = patient_data.pop('other_ids')
                        else:
                            other_ids = None
                        patient_data['birth_place'] = City.objects.get(pk=patient_data['birth_place'])
                        patient_data['city'] = City.objects.get(pk=patient_data['city'])
                        patient_form = PatientForm(patient_data)
                        if patient_form.is_valid():
                            cleaned_data = patient_form.cleaned_data
                            try:
                                patient = Patient.objects.get(pk=patient_id)
                                patient.update(**cleaned_data)
                                patient.save()
                                if other_ids:
                                    for identifier in other_ids:
                                        patient.other_ids.add(identifier)
                                    patient.save()
                                result[SUCCESS_KEY] = True
                                result[MESSAGE_KEY] = _('Patient %s successfully created' % patient.pk)
                                result[DATA_KEY] = patient.to_dictionary()
                            except Exception, e:
                                errors += u'%s\n' % e
                                result[ERRORS_KEY] = errors
                                result[SUCCESS_KEY] = False
                    except Exception, e:
                        errors += u'%s\n' % e
                        result[ERRORS_KEY] = errors
                        result[SUCCESS_KEY] = False
            except Exception, e:
                errors += u'%s\n' % e
                result[ERRORS_KEY] = errors
                result[SUCCESS_KEY] = False
        else:
            result[ERRORS_KEY] = _('POST method required.\n')
            result[SUCCESS_KEY] = False
    else:
        result[ERRORS_KEY] = _('Ajax data required.\n')
        result[SUCCESS_KEY] = False
    return HttpResponse(json.dumps(result), content_type='application/json; charset=utf8')


@require_POST
def activate(request):
    """Activate a patient, identified by his/her primary key"""
    result = {}
    errors = ''
    if request.method == 'POST':
        try:
            patient = Patient.objects.get(request.POST['id'])
            patient.active = True
            patient.save()
            result[SUCCESS_KEY] = True
            result[MESSAGE_KEY] = _('Patient %s is active' % request.POST['id'])
            result[DATA_KEY] = patient.to_dictionary()
        except Exception, e:
            errors += u'%s\n' % e
            result[ERRORS_KEY] = errors
            result[SUCCESS_KEY] = False
    else:
        result[ERRORS_KEY] = _('POST method required.\n')
        result[SUCCESS_KEY] = False
    return HttpResponse(json.dumps(result), content_type='application/json; charset=utf8')


@csrf_exempt
@require_POST
def deactivate(request):
    """Deactivate a patient, identified by his/her primary key"""
    result = {}
    errors = ''
    if request.method == 'POST':
        try:
            patient = Patient.objects.get(request.POST['id'])
            patient.active = False
            patient.save()
            result[SUCCESS_KEY] = True
            result[MESSAGE_KEY] = _('Patient %s is not active' % request.POST['id'])
            result[DATA_KEY] = patient.to_dictionary()
        except Exception, e:
            errors += u'%s\n' % e
            result[ERRORS_KEY] = errors
            result[SUCCESS_KEY] = False
    else:
        result[ERRORS_KEY] = _('POST method required.\n')
        result[SUCCESS_KEY] = False
    return HttpResponse(json.dumps(result), content_type='application/json; charset=utf8')


# TODO: Implement following views
def set_birth_place(request):
    """Create new City, if it doesn't exist, and set it as patient birth place"""
    result = {}
    return HttpResponse(json.dumps(result), content_type='application/json; charset=utf8')


def add_identifier(request):
    """Create new Identifier and add to other_identifiers"""
    result = {}
    return HttpResponse(json.dumps(result), content_type='application/json; charset=utf8')


def remove_identifier(request):
    """Set id disabled"""
    result = {}
    return HttpResponse(json.dumps(result), content_type='application/json; charset=utf8')


def set_city(request):
    result = {}
    return HttpResponse(json.dumps(result), content_type='application/json; charset=utf8')
