# -*- coding: utf-8 -*-
import os
import hashlib


def make_new_uid():
    return hashlib.sha1(os.urandom(20)).hexdigest()


def json_response():
    pass