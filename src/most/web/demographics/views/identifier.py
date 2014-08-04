#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils.translation import ugettext as _
import json
from datetime import date, datetime
from django.db.models import Q
from most.web.demographics.models import Patient, Identifier
from . import SUCCESS_KEY, MESSAGE_KEY, ERRORS_KEY, DATA_KEY, TOTAL_KEY
from most.web.demographics.forms import IdentifierForm


@csrf_exempt
@require_POST
def new(request):
    """Add new identifier, assuming only POST requests containing JSON data.

    POST JSON:
        {'type': String or None,
         'domain': String or None,
         'identifier': String}
    """
    result = {}
    errors = ''
    if request.is_ajax():
        if request.method == 'POST':
            # check required fields: identifier
            try:
                identifier_data = json.loads(request.body)
                mandatory_fields_checked = True
                for field in Identifier.MANDATORY_FIELDS:
                    try:
                        if field not in identifier_data:
                            errors += _('Field %s is mandatory\n' % field)
                            mandatory_fields_checked = False
                    except Exception, e:
                        errors += u'%s\n' % e
                if not mandatory_fields_checked:
                    result[ERRORS_KEY] = errors
                    result[SUCCESS_KEY] = False
                else:
                    try:
                        identifiers = Identifier.objects.filter(**identifier_data)
                        if not identifiers:
                            identifier = Identifier(**identifier_data)
                            identifier.save()
                            if identifier.pk:
                                result[SUCCESS_KEY] = True
                                result[MESSAGE_KEY] = _('Identifier %s successfully created.' % identifier.pk)
                                result[DATA_KEY] = identifier.to_dictionary()
                            else:
                                result[SUCCESS_KEY] = False
                                result[ERRORS_KEY] = _('Unable to save identifier.')
                        else:
                            identifier = identifiers[0]
                            result[SUCCESS_KEY] = True
                            result[MESSAGE_KEY] = _('Identifier %s already exists.' % identifier.pk)
                            result[DATA_KEY] = identifier.to_dictionary()
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
def filter(request):
    """Get a identifier by a query string"""
    result = {}
    errors = ''
    query_set = (Q())
    if request.method == 'GET':
        try:
            query_string = request.GET['query_string']
            query_list = [query for query in query_string.split(' ') if query]
            for query in query_list:
                query_set = query_set & (
                    Q(type__icontains=query) |
                    Q(domain__icontains=query) |
                    Q(identifier__icontains=query)
                )
            identifiers = Identifier.objects.filter(query_set)
            result[DATA_KEY] = []
            for identifier in identifiers:
                result[DATA_KEY].append(identifier.to_dictionary())
            if result[DATA_KEY]:
                result[MESSAGE_KEY] = _('%(identifiers_count)s identifiers found for query string: \'%(query_string)s\''
                                        % {'identifiers_count': identifiers.count(), 'query_string': query_string})
                result[TOTAL_KEY] = identifiers.count()
            else:
                result[MESSAGE_KEY] = _('No cities found for query string: \'%s\'' % query_string)
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
def edit(request, identifier_id):
    """Edit identifier data, assuming only POST requests containing JSON data.

    POST JSON:
        {'id': String,
         'type': String or None,
         'domain': String or None,
         'identifier': String}
    """
    result = {}
    errors = ''
    if request.method == 'POST':
        if request.is_ajax():
            # check required fields: first_name, last_name, gender, birth_date, birth_place
            try:
                identifier_data = json.loads(request.body)
                mandatory_fields_checked = True
                for field in Identifier.MANDATORY_FIELDS:
                    try:
                        if field not in identifier_data:
                            errors += _('Field %s is mandatory\n' % field)
                            mandatory_fields_checked = False
                    except Exception, e:
                        errors += u'%s\n' % e
                if not mandatory_fields_checked:
                    result[ERRORS_KEY] = errors
                    result[SUCCESS_KEY] = False
                else:
                    try:
                        identifier_form = IdentifierForm(identifier_data)
                        if identifier_form.is_valid():
                            cleaned_data = identifier_form.cleaned_data
                            try:
                                identifier = Identifier.objects.filter(pk=identifier_id)
                                identifier.update(**cleaned_data)
                                identifier = identifier[0]
                                result[SUCCESS_KEY] = True
                                result[MESSAGE_KEY] = _('Identifier %s successfully updated' % identifier.pk)
                                result[DATA_KEY] = identifier.to_dictionary()
                            except Exception, e:
                                errors += u'%s\n' % e
                                result[ERRORS_KEY] = errors
                                result[SUCCESS_KEY] = False
                        else:
                            for error in identifier_form.errors:
                                errors += u'%s: %s' % (error, identifier_form.errors[error])
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
            result[ERRORS_KEY] = _('Ajax data required.\n')
            result[SUCCESS_KEY] = False
    else:
        result[ERRORS_KEY] = _('POST method required.\n')
        result[SUCCESS_KEY] = False
    return HttpResponse(json.dumps(result), content_type='application/json; charset=utf8')


def get_patient(request):
    pass