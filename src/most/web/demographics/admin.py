#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

# -*- coding: utf-8 -*-
from django.contrib import admin
from most.web.demographics.models import Patient, City, Identifier


class PatientAdmin(admin.ModelAdmin):
    exclude = ['uid', 'deactivation_timestamp']


# Register your models here.
admin.site.register(Patient, PatientAdmin)
admin.site.register(City)
admin.site.register(Identifier)

