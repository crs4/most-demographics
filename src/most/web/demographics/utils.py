# -*- coding: utf-8 -*-
#
# Project MOST - Moving Outcomes to Standard Telemedicine Practice
# http://most.crs4.it/
#
# Copyright 2014, CRS4 srl. (http://www.crs4.it/)
# Dual licensed under the MIT or GPL Version 2 licenses.
# See license-GPLv2.txt or license-MIT.txt

import os
import re
import uuid
import socket
import hashlib

from django.conf import settings

from hl7apy import load_message_profile, VALIDATION_LEVEL as VL
from hl7apy.core import Message
from hl7apy.parser import parse_message

_MP_ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hl7_profiles")
_PDQ_REQ_MP = load_message_profile(os.path.join(_MP_ROOT_PATH, "pdq_request"))
_PDQV_REQ_MP = load_message_profile(os.path.join(_MP_ROOT_PATH, "pdqv_request"))
_PDQ_RES_MP = load_message_profile(os.path.join(_MP_ROOT_PATH, "pdq_response"))
_PDQV_RES_MP = load_message_profile(os.path.join(_MP_ROOT_PATH, "pdqv_response"))


def make_new_uid():
    return hashlib.sha1(os.urandom(20)).hexdigest()


def json_response():
    pass


def send_hl7_message(host, port, er7_message):
    sb = "\x0b"
    eb = "\x1c"
    cr = "\x0d"

    validator = "{0}{1}{2}{3}".format(sb, "(([^\r]+\r)*([^\r]+\r?))", eb, cr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        # send the message
        sock.sendall(er7_message)
        # receive the answer
        received = sock.recv(1024*1024)
        res = re.match(validator, received)
        if res is not None:
            res = res.groups()[0]
    except socket.error:
        res = None
    finally:
        sock.close()
    return res


def send_pdq_request(patient_id):
    try:
        host, port = settings.MLLP_HOST, settings.MLLP_PORT
    except AttributeError:
        raise AttributeError("Couldn't find MLLP_HOST or MLLP_PORT in the settings file. Did you set them?")

    msg = Message("QBP_Q21", reference=_PDQ_REQ_MP)
    msh_9 = "QBP^Q22^QBP_Q21"
    msg.msh.msh_3 = "MOST CLIENT"
    msg.msh.msh_4 = "MOST DEMOGRAPHICS"
    msg.msh.msh_5 = "MOST SERVER"
    msg.msh.msh_6 = "MOST DEMO"
    msg.msh.msh_9 = msh_9
    msg.msh.msh_10 = uuid.uuid4().hex[:20]
    msg.msh.msh_11 = "P"
    msg.msh.msh_17 = "ITA"
    msg.msh.msh_18 = "UTF-8"
    msg.msh.msh_19 = "IT"

    msg.qpd.qpd_1 = "IHE PDQ Query"
    msg.qpd.qpd_2 = uuid.uuid4().hex[:20]
    msg.qpd.add_field("qpd_3").value = "@PID.3.1^{}".format(patient_id)

    msg.rcp.rcp_1 = "I"

    res = send_hl7_message(host, port, msg.to_mllp())

    return parse_pdq_response(res)


def parse_pdq_response(er7_message):
    print er7_message
    msg = parse_message(er7_message, message_profile=_PDQ_RES_MP, validation_level=VL.TOLERANT)

    msg_status = msg.msa.msa_1.value
    query_status = msg.qak.qak_2.value

    if msg_status != "AA":
        return None
    if query_status == "NF":
        return []

    patients = []
    for g in msg.rsp_k21_query_response:
        patient = {
            "IDENTIFIERS": [],
            "NAME": g.pid.pid_5.xpn_2.value,
            "SURNAME": g.pid.pid_5.xpn_1.value,
            "DATETIME_OF_BIRTH": g.pid.pid_7.ts_1.value,
            "ADMINISTRATIVE_SEX": g.pid.pid_8.value,
            "ACCOUNT_NUMBER": g.pid.pid_18.cx_1.value,
            "BIRTH_PLACE": g.pid.pid_23.value
        }
        for p in g.pid.pid_3:
            patient["IDENTIFIERS"].append({
                "DOMAIN": p.cx_4.hd_1.value.value,
                "VALUE": p.cx_1.value
            })

        patients.append(patient)

    return patients
