# -*- coding: utf-8 -*-
from django.contrib import admin
from demographics.models import Patient, City, Identifier


class PatientAdmin(admin.ModelAdmin):
    exclude = ['uid', 'deactivation_timestamp']


# Register your models here.
admin.site.register(Patient, PatientAdmin)
admin.site.register(City)
admin.site.register(Identifier)

