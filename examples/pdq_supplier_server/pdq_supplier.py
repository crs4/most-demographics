import os
import uuid
import logging
import datetime

from hl7apy.v2_5 import DTM
from hl7apy.utils import check_date
from hl7apy.mllp import AbstractHandler
from hl7apy.parser import parse_message
from hl7apy.core import Message
from hl7apy import load_message_profile

from dao import DAO

_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

PDQ_REQ_MP = load_message_profile(os.path.join(_ROOT_PATH, './pdq_req'))
PDQ_RES_MP = load_message_profile(os.path.join(_ROOT_PATH, './pdq_res'))

logger = logging.getLogger(__name__)


class PDQHandler(AbstractHandler):

    REQ_MP, RES_MP = PDQ_REQ_MP, PDQ_RES_MP
    PDQ_FIELD_NAMES = {
        '@PID.3.1': "IDENTIFIER",
        '@PID.5.1.1': 'SURNAME',
        '@PID.5.2': 'NAME',
        '@PID.7.1': 'DOB'
    }

    def __init__(self, message):
        self.dao = DAO()
        msg = parse_message(message, message_profile=self.REQ_MP)
        super(PDQHandler, self).__init__(msg)

    def _create_res(self, ack_code, patients):
        res = Message('RSP_K21', reference=self.RES_MP)
        r, q = res.msh, self.incoming_message.msh
        r.msh_5, r.msh_6 = q.msh_3, q.msh_4
        res.msh.msh_5 = self.incoming_message.msh.msh_3
        res.msh.msh_6 = self.incoming_message.msh.msh_4
        r.msh_7.ts_1 = DTM(datetime.datetime.now())
        r.msh_9 = 'RSP^K22^RSP_K21'
        r.msh_10 = uuid.uuid4().hex

        r, q = res.msa, self.incoming_message.msh
        r.msa_1 = ack_code
        r.msa_2 = q.msh_10.msh_10_1

        r, q = res.qak, self.incoming_message.qpd
        r.qak_1 = q.qpd_2
        r.qak_2 = ('OK'
                   if len(patients) > 0 else 'NF')
        r.qak_4 = str(len(patients))

        res.qpd = self.incoming_message.qpd
        g = res.add_group('rsp_k21_query_response')
        for i, p in enumerate(patients):
            s = g.add_segment('PID')
            s.pid_1 = str(i)
            s.pid_3.cx_1 = p["IDENTIFIER"]
            s.pid_3.cx_4 = "master"
            s.pid_5 = "%s^%s" % (p["SURNAME"], p["NAME"])
            s.pid_7.ts_1 = p["DATETIME_OF_BIRTH"]
            s.pid_8 = p["ADMINISTRATIVE_SEX"]
            s.pid_18.cx_1 = p["ACCOUNT_NUMBER"]
            s.pid_23 = p["BIRTH_PLACE"]
        return res

    def _create_err(self, code, desc):
        res = self._create_res('AR', 'AR', [])
        res.err.err_1, res.err.err_2 = code, desc
        return res

    def reply(self):
        logger.info("Received message:\n{}".format(self.incoming_message.to_er7().replace("\r", "\n")))

        params = dict((self.PDQ_FIELD_NAMES[q.qip_1.value], q.qip_2.value)
                      for q in self.incoming_message.qpd.qpd_3
                      if q.qip_1.value in self.PDQ_FIELD_NAMES)

        logger.info("Extracted parameters: {}".format(params))

        if '' in params.values() or ('DOB' in params and not check_date(params.get('DOB'))):
            return self._create_err("100", "Invalid params")
        else:
            p = self.dao.get_data(params)

        res = self._create_res('AA', p)
        res = res.to_mllp()
        logger.info("Sending result: {}".format(res.replace("\r", "\n")))
        return res
