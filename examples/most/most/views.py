# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.http import Http404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.utils.translation import get_language


def index(request):
    context = RequestContext(request)
    context.update(csrf(request))
    return render_to_response('base.html', context)


def examples(request):
    context = RequestContext(request)
    context.update(csrf(request))
    response = render_to_response('demographics/demo.html', context)
    response.set_cookie("django_language", get_language())
    return response
