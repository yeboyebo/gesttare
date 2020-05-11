
# @class_declaration gesttare #
from YBLEGACY.constantes import *
from YBUTILS.APIQSA import APIQSA
import traceback
import sys

class gesttare(interna):

    def gesttare_borrarAdjuntoTarea(self, model, oParam):
        # iddocumento = model.iddocumento
        # idUsuario = qsatype.FLUtil.nameUser()
        # resul = {}
        # try:
        #     params = {
        #         'pk': iddocumento
        #     }
        #     APIQSA.entry_point('post', "gd_documentos", idUsuario, params, 'delete')

        # except Exception as e:
        #     print('Excepcion', str(e))

        #     ex_type, ex_value, ex_traceback = sys.exc_info()

        #     # Extract unformatter stack traces as tuples
        #     trace_back = traceback.extract_tb(ex_traceback)

        #     # Format stacktrace
        #     stack_trace = list()

        #     for trace in trace_back:
        #         stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        #     print("Exception type : %s " % ex_type.__name__)
        #     print("Exception message : %s" %ex_value)
        #     print("Stack trace : %s" %"\n".join(stack_trace))

        #     raise(e)

        # resul["return_data"] = False
        # resul["msg"] = "Adjunto eliminado"
        iddocumento = model.iddocumento
        idUsuario = qsatype.FLUtil.nameUser()
        resul = {}
        if "confirmacion" in oParam and oParam["confirmacion"]:
            params = {
                'pk': iddocumento
            }
            msg = "Adjunto eliminado"
            if not APIQSA.entry_point('post', "gd_documentos", idUsuario, params, 'delete'):
                msg = "Error al eliminar adjunto"
                resul['status'] = 1
            resul["return_data"] = False
            resul["msg"] = msg
            return resul


        resul['status'] = 2
        resul["confirm"] = "El adjunto será eliminado"
        resul["serverAction"] = "borrarAdjuntoTarea"
        # return resul
        return resul

    def __init__(self, context=None):
        super().__init__(context)

    def borrarAdjuntoTarea(self, model, oParam):
        return self.ctx.gesttare_borrarAdjuntoTarea(model, oParam)

