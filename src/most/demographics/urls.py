# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from demographics.views import patient, city, identifier

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'most.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
)

# Patient API related urls
urlpatterns += patterns('',
    (r'^patient/new/$', patient.new),
    (r'^patient/get/$', patient.get),
    (r'^patient/(?P<patient_id>\d+)/edit/$', patient.edit),
    (r'^patient/(?P<patient_id>\d+)/deactivate/$', patient.deactivate),
    (r'^patient/(?P<patient_id>\d+)/activate/$', patient.activate),
    (r'^patient/(?P<patient_id>\d+)/add_id/$', patient.add_identifier),
    (r'^patient/(?P<patient_id>\d+)/remove_id/$', patient.remove_identifier),
    (r'^patient/(?P<patient_id>\d+)/set_birth_place/$', patient.set_birth_place),
    (r'^patient/(?P<patient_id>\d+)/set_city/$', patient.set_city),
    #(r"^patient/delete/$", patient.delete),
    #(r'^patient/get/all/$', 'get_all_patients'),
    #(r'^patient/get/active/$', 'get_active_patients'),
    #(r'^patient/get/oauth/$', 'get_active_patients_oauth'),
    #(r'^patient/add_task_group/$', 'add_task_group_to_patient'),
    #(r'^patient/get_task_groups/$', 'get_task_groups'),
    #(r'^patient/(?P<patient_id>\d+)/get_medicalrecords/$', 'get_medicalrecords'),
    #(r'^api/patient/get_contacts/$', 'get_contacts'),
)

# City API related urls
urlpatterns += patterns('',
    (r'^city/new/$', city.new),
    (r'^city/get/$', city.get),
    (r'^city/(?P<city_id>\d+)/edit/$', city.edit),
)

# Identifier API related urls
urlpatterns += patterns('',
    (r'^identifier/new/$', identifier.new),
    (r'^identifier/get/$', identifier.get),
    (r'^identifier/(?P<identifier_id>\d+)/edit/$', identifier.edit),
    (r'^identifier/(?P<identifier_id>\d+)/get_patient/$', identifier.get_patient),
)
