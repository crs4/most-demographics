import logging


from hl7apy.mllp import MLLPServer, AbstractErrorHandler

from pdq_supplier import PDQHandler
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')


class ErrorHandler(AbstractErrorHandler):
    def reply(self):
        print self.exc
        return None

message_handlers = {'QBP^Q22^QBP_Q21': (PDQHandler,),
                    'ERR': (ErrorHandler, )}

srvr = MLLPServer(host='localhost', port=2575, handlers=message_handlers)
srvr.serve_forever()