# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from datetime import datetime

from YBLEGACY.constantes import *
from YBUTILS.viewREST import cacheController


class gesttare(interna):

    def gesttare_getDesc(self):
        return None

    def gesttare_start(self, model):
        now = str(qsatype.Date())
        hora = now[-8:]
        user_name = qsatype.FLUtil.nameUser()

        response = {}
        response["resul"] = False
        response["msg"] = ""

        if qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idusuario = '{}' AND horafin IS NULL".format(user_name)):
            response["msg"] = "Ya existe un tramo iniciado"
            return response

        if not qsatype.FLUtil().sqlInsert("gt_controlhorario", ["horainicio", "idusuario"], [hora, user_name]):
            response["msg"] = "Error al crear el registro horario"
            return response

        response["resul"] = True
        response["msg"] = "Iniciado"
        return response

    def gesttare_pause(self, model):
        now = str(qsatype.Date())
        hora = now[-8:]
        user_name = qsatype.FLUtil.nameUser()

        response = {}
        response["resul"] = False
        response["msg"] = ""

        if not qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idusuario = '{}' AND horafin IS NULL".format(user_name)):
            response["msg"] = "No existe un tramo iniciado"
            return response

        if not qsatype.FLUtil().sqlUpdate("gt_controlhorario", ["horafin"], [hora], "idusuario = '{}' AND horafin IS NULL".format(user_name)):
            response["msg"] = "Error al actualizar el registro horario"
            return response

        response["resul"] = True
        response["msg"] = "Detenido"
        return response

    def gesttare_check_permissions(self, model, prefix, pk, template, acl, accion):
        if template == "formRecord":
            my_name = qsatype.FLUtil.nameUser()

            reg_name = qsatype.FLUtil.sqlSelect("gt_controlhorario", "idusuario", "idc_horario = {}".format(pk))
            if my_name == str(reg_name):
                return True

            return False

        return True

    def gesttare_get_estado(self):
        estado = cacheController.getSessionVariable("estado_controlhorario", None)

        if not estado:
            self.iface.set_estado("diario")
            estado = "diario"

        return estado

    def gesttare_set_estado(self, estado):
        cacheController.setSessionVariable("estado_controlhorario", estado)
        return True

    def gesttare_drawif_controldiario(self, cursor):
        if self.iface.get_estado() != "diario":
            return "hidden"

    def gesttare_drawif_controlmensual(self, cursor):
        if self.iface.get_estado() != "mensual":
            return "hidden"

    def gesttare_drawif_botondiario(self, cursor):
        if self.iface.get_estado() == "diario":
            return "disabled"

    def gesttare_drawif_botonmensual(self, cursor):
        if self.iface.get_estado() == "mensual":
            return "disabled"

    def gesttare_drawif_horaeditable(self, cursor):
        if qsatype.FLUtil().quickSqlSelect("gt_controldiario", "validado", "idc_diario = {}".format(cursor.valueBuffer("idc_diario"))):
            return "disabled"

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def start(self, model):
        return self.ctx.gesttare_start(model)

    def pause(self, model):
        return self.ctx.gesttare_pause(model)

    def check_permissions(self, model, prefix, pk, template, acl, accion=None):
        return self.ctx.gesttare_check_permissions(model, prefix, pk, template, acl, accion)

    def drawif_controldiario(self, cursor):
        return self.ctx.gesttare_drawif_controldiario(cursor)

    def drawif_controlmensual(self, cursor):
        return self.ctx.gesttare_drawif_controlmensual(cursor)

    def drawif_botondiario(self, cursor):
        return self.ctx.gesttare_drawif_botondiario(cursor)

    def drawif_botonmensual(self, cursor):
        return self.ctx.gesttare_drawif_botonmensual(cursor)

    def drawif_horaeditable(self, cursor):
        return self.ctx.gesttare_drawif_horaeditable(cursor)

    def get_estado(self):
        return self.ctx.gesttare_get_estado()

    def set_estado(self, estado):
        return self.ctx.gesttare_set_estado(estado)


# @class_declaration head #
class head(gesttare):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
