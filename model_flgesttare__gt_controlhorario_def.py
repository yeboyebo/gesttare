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
from models.flgesttare import flgesttare_def


class gesttare(interna):

    def gesttare_getDesc(self):
        return None

    def gesttare_start(self, model):
        user_name = qsatype.FLUtil.nameUser()
        now = str(qsatype.Date())
        fecha = now[:10]
        hora = now[-8:]

        curDiario = qsatype.FLSqlCursor(u"gt_controldiario")
        curDiario.select(ustr(u"fecha = '", fecha, u"' AND idusuario = '", user_name, "'"))
        if curDiario.next():
            print("este es el start")
            print("hay que ver que no haya un tramo en la hora a la que quieres empezar a trackear")
            curHorario = qsatype.FLSqlCursor(u"gt_controlhorario")
            curHorario.select(ustr(u"idc_diario = '", curDiario.valueBuffer("idc_diario"), u"'"))
            while curHorario.next():
                curHorario.setModeAccess(curHorario.Browse)
                curHorario.refreshBuffer()
                horaInicio = flgesttare_def.iface.time_to_seconds(hora)
                anteriorInicio = flgesttare_def.iface.time_to_seconds((curHorario.valueBuffer("horainicio")))
                anteriorFin = flgesttare_def.iface.time_to_seconds((curHorario.valueBuffer("horafin")))
                if (horaInicio > anteriorInicio and horaInicio < anteriorFin):
                    resul = {}
                    resul["status"] = 1
                    resul["msg"] = "Error ya existe un tramo en este horario"
                    return resul

        mes = str(fecha).split("-")[1]
        response = {}
        response["resul"] = False
        response["msg"] = ""
        if qsatype.FLUtil().quickSqlSelect("gt_controldiario", "validado", "fecha = '{}' AND idusuario = '{}'".format(now[:10], user_name)):
            response["status"] = 1
            response["msg"] = "El dia ya esta validado"
            return response

        if qsatype.FLUtil().quickSqlSelect("gt_controlmensual", "validado_user", "mes = '{}' AND idusuario = '{}'".format(mes, user_name)):
            response["status"] = 1
            response["msg"] = "El mes ya esta validado por el usuario"
            return response

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

            im_superuser = qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(my_name))
            if im_superuser:
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

    def gesttare_drawif_idusuariofilter(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        isSuperuser = qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(usuario))
        if not isSuperuser:
            return "hidden"
        return True

    def gesttare_get_model_info(self, model, data, ident, template, where_filter):
        if template == "control_diario":
            user_name = qsatype.FLUtil.nameUser()
            user_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(user_name))
            where = "aqn_user.idcompany = " + str(user_company)
            if where_filter:
                where += " AND " + where_filter
            tiempototal = qsatype.FLUtil.quickSqlSelect("gt_controldiario INNER JOIN aqn_user ON gt_controldiario.idusuario = aqn_user.idusuario", "SUM(horasordinarias)", where) or 0
            tiempototal = flgesttare_def.iface.seconds_to_time(tiempototal, all_in_hours=True)
            return {"queryGridcontroldiario": "Tiempo total: {}".format(tiempototal)}

        if template == "newrecord":
            fecha = qsatype.FLUtil().quickSqlSelect("gt_controldiario", "fecha", "idc_diario = {}".format(data["idc_diario"]))
            formateaFecha = str(fecha).split("-")
            return {"chForm": "Nuevo registro para " + formateaFecha[2] + "-" + formateaFecha[1] + "-" + formateaFecha[0]}

        return None

    def gesttare_queryGrid_control_diario(self, model, filters):
        where = ""
        user_name = qsatype.FLUtil.nameUser()
        user_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(user_name))
        if qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(user_name)):
            where += "aqn_user.idcompany = " + str(user_company)
        else:
            where += "gt_controldiario.idusuario = '" + str(user_name) + "'"
        if filters:
            if "[gt_controldiario.idusuario]" in filters and filters["[gt_controldiario.idusuario]"] != "":
                where += " AND gt_controldiario.idusuario = '{}'".format(filters["[gt_controldiario.idusuario]"])
            if "[d_gt_controldiario.fecha]" in filters and filters["[d_gt_controldiario.fecha]"] != "":
                where += " AND gt_controldiario.fecha >= '{}'".format(filters["[d_gt_controldiario.fecha]"])
            if "[h_gt_controldiario.fecha]" in filters and filters["[h_gt_controldiario.fecha]"] != "":
                where += " AND gt_controldiario.fecha <= '{}'".format(filters["[h_gt_controldiario.fecha]"])
            if "[gt_controldiario.fecha]" in filters and filters["[gt_controldiario.fecha]"] != "" and filters["[d_gt_controldiario.fecha]"] == "" and filters["[h_gt_controldiario.fecha]"] == "":
                where += " AND gt_controldiario.fecha = '{}'".format(filters["[gt_controldiario.fecha]"])
        #     if "[buscador]" in filters and filters["[buscador]"] != "":
        #         where += " AND UPPER(gt_proyectos.nombre) LIKE '%" + filters["[buscador]"].upper() + "%' OR UPPER(gt_tareas.nombre) LIKE '%" + filters["[buscador]"].upper() + "%' OR UPPER(aqn_user.nombre) LIKE '%" + filters["[buscador]"].upper() + "%'"

        query = {}
        query["tablesList"] = ("gt_controldiario, aqn_user")
        query["select"] = ("gt_controldiario.idc_diario, gt_controldiario.idusuario, gt_controldiario.fecha, aqn_user.usuario, gt_controldiario.horaentrada, gt_controldiario.horasalida, gt_controldiario.totaltiempostring, gt_controldiario.horasextra, gt_controldiario.validado")
        query["from"] = ("gt_controldiario INNER JOIN aqn_user ON gt_controldiario.idusuario = aqn_user.idusuario")
        query["where"] = (where)
        query["orderby"] = ("gt_controldiario.fecha DESC, gt_controldiario.idusuario")

        return query

    def gesttare_validateCursor(self, cursor):
        if cursor.valueBuffer("idc_diario"):
            horaInicio = flgesttare_def.iface.time_to_seconds((cursor.valueBuffer("horainicio")))
            horaFin = flgesttare_def.iface.time_to_seconds((cursor.valueBuffer("horafin")))
            curHorario = qsatype.FLSqlCursor(u"gt_controlhorario")
            curHorario.select(ustr(u"idc_diario = '", cursor.valueBuffer("idc_diario"), u"' AND idc_horario <> '", cursor.valueBuffer("idc_horario"), "'"))
            while curHorario.next():
                curHorario.setModeAccess(curHorario.Browse)
                curHorario.refreshBuffer()
                anteriorInicio = flgesttare_def.iface.time_to_seconds((curHorario.valueBuffer("horainicio")))
                anteriorFin = flgesttare_def.iface.time_to_seconds((curHorario.valueBuffer("horafin")))
                if (horaInicio > anteriorInicio and horaInicio < anteriorFin) or (horaFin > anteriorInicio and horaFin < anteriorFin) or (anteriorInicio > horaInicio and anteriorInicio < horaFin):
                    qsatype.FLUtil.ponMsgError("Los registors horarios se solapan")
                    return False
        return True

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

    def drawif_idusuariofilter(self, cursor):
        return self.ctx.gesttare_drawif_idusuariofilter(cursor)

    def get_estado(self):
        return self.ctx.gesttare_get_estado()

    def set_estado(self, estado):
        return self.ctx.gesttare_set_estado(estado)

    def get_model_info(self, model, data, ident, template, where_filter):
        return self.ctx.gesttare_get_model_info(model, data, ident, template, where_filter)

    def queryGrid_control_diario(self, model, filters):
        return self.ctx.gesttare_queryGrid_control_diario(model, filters)

    def validateCursor(self, cursor):
        return self.ctx.gesttare_validateCursor(cursor)


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
