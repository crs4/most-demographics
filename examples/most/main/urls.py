# -*- coding: utf-8 -*-
#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'most.main.views.index', name='index'),
    url(r'^demo/', 'most.main.views.examples', name='examples'),
    url(r'^examples/', 'most.main.views.examples', name='examples'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^demographics/', include('most.web.demographics.urls', namespace='demographics')), #urls of demographics app api
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
