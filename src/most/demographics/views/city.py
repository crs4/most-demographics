# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _
import json
from datetime import date, datetime
from django.db.models import Q
from demographics.models import Patient, City, Identifier
from django.conf import settings
from demographics.views import SUCCESS_KEY, MESSAGE_KEY, ERRORS_KEY, DATA_KEY, TOTAL_KEY


@csrf_exempt
@require_POST
def new(request):
    """Add new city, assuming only POST requests containing JSON data.

    POST JSON:
        {'name': String,
         'province': String or None,
         'state': String,
         'code': String or None}
    """
    result = {}
    errors = ''
    if request.is_ajax():
        if request.method == 'POST':
            # check required fields: name, state
            try:
                city_data = json.loads(request.body)
                mandatory_fields_checked = True
                for field in City.MANDATORY_FIELDS:
                    try:
                        if field not in city_data or not city_data[field]:
                            errors += _('Field %s is mandatory.\n' % field)
                            mandatory_fields_checked = False
                    except Exception, e:
                        errors += u'%s\n' % e
                if not mandatory_fields_checked:
                    result[ERRORS_KEY] = errors
                    result[SUCCESS_KEY] = False
                else:
                    try:
                        cities = City.objects.filter(**city_data)
                        if not cities:
                            city = City(**city_data)
                            city.save()
                            if city.pk:
                                result[SUCCESS_KEY] = True
                                result[MESSAGE_KEY] = _('City %s successfully created.' % city.pk)
                                result[DATA_KEY] = city.to_dictionary()
                            else:
                                result[SUCCESS_KEY] = False
                                result[ERRORS_KEY] = _('Unable to save city.')
                        else:
                            city = cities[0]
                            result[SUCCESS_KEY] = True
                            result[MESSAGE_KEY] = _('City %s already exists.' % city.pk)
                            result[DATA_KEY] = city.to_dictionary()
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
    """Get a city by a query string"""
    result = {}
    errors = ''
    query_set = (Q())
    if request.method == 'GET':
        try:
            query_string = request.GET['query_string']
            query_list = [query for query in query_string.split(' ') if query]
            for query in query_list:
                query_set = query_set & (
                    Q(name__icontains=query) |
                    Q(province__icontains=query) |
                    Q(state__icontains=query) |
                    Q(code__icontains=query)
                )
            cities = City.objects.filter(query_set)
            result[DATA_KEY] = []
            for city in cities:
                result[DATA_KEY].append(city.to_dictionary())
            if result[DATA_KEY]:
                result[MESSAGE_KEY] = _('%(cities_count)s cities found for query string: \'%(query_string)s\'' %
                                        {'cities_count': cities.count(), 'query_string': query_string})
                result[TOTAL_KEY] = cities.count()
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


@require_POST
def edit(request):
    pass