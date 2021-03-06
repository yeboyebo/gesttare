# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
from models.flgesttare import flgesttare_def
from datetime import datetime, timedelta

class gesttare(interna):

    def gesttare_getDesc(self):
        return None

    def gesttare_getForeignFields(self, model, template=None):
        fields = [
            {'verbose_name': 'usuario', 'func': 'field_usuario'},
            {'verbose_name': 'completaIcon', 'func': 'field_completaIcon'},
            {'verbose_name': 'completaTitle', 'func': 'field_completaTitle'}
        ]

        return fields

    def gesttare_field_usuario(self, model):
        nombre_usuario = ""

        try:
            if not model.idusuario:
                return nombre_usuario
            nombre_usuario = model.idusuario.usuario
        except Exception:
            pass

        return nombre_usuario

    def gesttare_check_permissions(self, model, prefix, pk, template, acl, accion):
        if template == "formRecord":
            my_name = qsatype.FLUtil.nameUser()
            if my_name == "admin":
                return True

            reg_name = qsatype.FLUtil.sqlSelect("gt_controldiario", "idusuario", "idc_diario = {}".format(pk))
            responsable = qsatype.FLUtil.sqlSelect("aqn_user", "idresponsable", "idusuario = '{}'".format(reg_name))
            if my_name == str(reg_name):
                return True

            im_superuser = qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(my_name))
            if im_superuser:
                return True

            if str(responsable) == str(my_name):
                return True



            # my_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(my_name))
            # reg_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(reg_name))
            # if my_company == reg_company:
            #     return True

            return False

        return True

    def gesttare_getFilters(self, model, name, template=None):
        filters = []

        if name == "regusuario":
            user_name = qsatype.FLUtil.nameUser()
            filters = [{"criterio": "idusuario__exact", "valor": user_name, "tipo": "q"}]

            if not qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(user_name)):
                return filters

            usuarios = []
            user_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(user_name))

            q = qsatype.FLSqlQuery()
            q.setSelect("idusuario")
            q.setFrom("aqn_user")
            q.setWhere("idcompany = {}".format(user_company))

            if not q.exec_():
                return False

            while q.next():
                usuarios.append(q.value(0))

            filters.append({"criterio": "idusuario__in", "valor": usuarios, "tipo": "q"})

        return filters

    def gesttare_drawif_validar(self, cursor):
        if cursor.valueBuffer("validado"):
            return "hidden"

        if qsatype.FLUtil.nameUser() != str(cursor.valueBuffer("idusuario")):
            return "disabled"

        # if not cursor.valueBuffer("horasextra"):
        #     return "disabled"

        if qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idc_diario = {} AND horafin IS NULL".format(cursor.valueBuffer("idc_diario"))):
            return "disabled"
            
    def gesttare_drawif_borrarButton(self, cursor):
        if cursor.valueBuffer("validado"):
            return "hidden"

        if qsatype.FLUtil.nameUser() != str(cursor.valueBuffer("idusuario")):
            return "disabled"

        # if not cursor.valueBuffer("horasextra"):
        #     return "disabled"

        if qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idc_diario = {} AND horafin IS NULL".format(cursor.valueBuffer("idc_diario"))):
            return "hidden"

    def gesttare_drawif_desbloquear(self, cursor):
        if cursor.valueBuffer("validado"):
            return True

        if qsatype.FLUtil.nameUser() != str(cursor.valueBuffer("idusuario")):
            return "hidden"

        if qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idc_diario = {} AND horafin IS NULL".format(cursor.valueBuffer("idc_diario"))):
            return "hidden"

        return "hidden"

    def gesttare_drawif_nuevotramo(self, cursor):
        if cursor.valueBuffer("validado"):
            return "hidden"

        if qsatype.FLUtil.nameUser() != str(cursor.valueBuffer("idusuario")):
            return "hidden"

    def gesttare_drawif_horasextra(self, cursor):
        if cursor.valueBuffer("validado"):
            return "disabled"

        if qsatype.FLUtil.nameUser() != str(cursor.valueBuffer("idusuario")):
            return "disabled"

    def gesttare_validar(self, model, oParam, cursor):
        if qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idc_diario = {} AND horafin IS NULL".format(cursor.valueBuffer("idc_diario"))):
            response = {}
            response["status"] = 1
            response["msg"] = "No puedes validar el día si tienes un tramo activo"
            return response
        if "confirmacion" not in oParam:
            resul = {}
            if cursor.valueBuffer("horasextra"):
                if cursor.valueBuffer("horasordinarias") < flgesttare_def.iface.time_to_seconds(cursor.valueBuffer("horasextra")):
                    resul["status"] = 1
                    resul["msg"] = "Las horas extraordinarias no pueden superar el total de tiempo"
                    return resul
            resul['status'] = 2
            horasextra = cursor.valueBuffer("horasextra") or "00:00:00"
            horasordinarias = cursor.valueBuffer("horasordinariasstring") or "00:00:00"
            resul['confirm'] = "Vas a validar el día con los siguientes datos: " + str(horasordinarias) + " como tiempo de trabajo ordinario, y " + str(horasextra) + " como tiempo de trabajo extraordinario. ¿Son correctos los datos?"
            return resul
        else:
            if cursor.valueBuffer("validado"):
                return True

            cursor.setValueBuffer("validado", True)
            if not cursor.commitBuffer():
                return False
            resul = {}
            # resul['status'] = True
            resul["msg"] = "Día validado correctamente"
            return resul
        return True

    def gesttare_validar_dia(self, model, oParam, cursor):
        if cursor.valueBuffer("validado"):
            # resul = {}
            # resul["status"] = 1
            # resul["msg"] = "El día ya esta validado"
            # return resul
            return self.iface.desbloquear(model, oParam, cursor)
        return self.iface.validar(model, oParam, cursor)

    def gesttare_borrar_dia(self, model, oParam, cursor):
        resul = {}
        if not cursor.valueBuffer("validado"):
            if "confirmacion" not in oParam:
                fecha = cursor.valueBuffer("fecha")
                resul['status'] = 2
                resul['confirm'] = "Vas a eliminar el registro diario con fecha: " + str(datetime.strptime(fecha, '%Y-%m-%d').strftime("%d/%m/%y")) + ". ¿Quieres continuar?"
                return resul
            else:
                usuario = qsatype.FLUtil.nameUser()
                # control_horario = qsatype.FLSqlCursor("gt_controlhorario")
                # control_horario.select("idusuario = " + str(usuario) + " AND idc_diario = " + str(cursor.valueBuffer("idc_diario")))
                # control_horario.setModeAccess(control_horario.Del)
                # control_horario.refreshBuffer()
                # if not control_horario.commitBuffer():
                #     return False
                if not qsatype.FLUtil.sqlDelete("gt_controlhorario", "idusuario = " + str(usuario) + " AND idc_diario = " + str(cursor.valueBuffer("idc_diario"))):
                    return False
                cursor.setModeAccess(cursor.Del)
                cursor.refreshBuffer()
                if not cursor.commitBuffer():
                    return False
                resul["return_data"] = False
                resul["msg"] = "Registro diario eliminado"
                return resul
        else:
            resul['status'] = 1
            resul["msg"] = "No se puede eliminar un registro diario validado"
            return resul
        return True

    def gesttare_desbloquear(self, model, oParam, cursor):
        mesvalid = qsatype.FLUtil.sqlSelect("gt_controlmensual", "validado_user", "idc_mensual = {}".format(cursor.valueBuffer("idc_mensual")))
        if mesvalid:
            resul = {}
            resul['status'] = 1
            resul['msg'] = "Error. Debes desbloquear primero el mes"
            return resul
        if "confirmacion" not in oParam:
            resul = {}
            resul['status'] = 2
            resul['confirm'] = "Vas a desbloquear el día"
            return resul
        else:

            if not cursor.valueBuffer("validado"):
                return True

            cursor.setValueBuffer("validado", False)
            if not cursor.commitBuffer():
                return False
            resul = {}
            # resul['status'] = True
            resul["msg"] = "Día desbloqueado correctamente"
            return resul

        return True

    def gesttare_gotoNuevoTramoFecha(self, model, oParam):
        tengopermiso = flgesttare_def.iface.compruebaPermisosPlan("start")
        if tengopermiso != True:
            return tengopermiso

        resul = {}
        resul['status'] = 1
        # oParam["fecha"] = "2020-05-12"
        # print("el valor es: ",oParam["fecha"])
        if "fecha" in oParam:
            user_name = qsatype.FLUtil.nameUser()

            idc_diario = qsatype.FLUtil().quickSqlSelect("gt_controldiario", "idc_diario", "idusuario = '{}' AND fecha = '{}'".format(user_name, oParam["fecha"]))
            if idc_diario:
                resul["msg"] = "Ya existe un registro para tu usaurio en el dia " + oParam["fecha"]
                return resul
            if not idc_diario:
                if not qsatype.FLUtil().sqlInsert("gt_controldiario", ["fecha", "horaentrada", "horasextra", "idusuario"], [oParam["fecha"], "00:00:01", "00:00:00", user_name]):
                    resul["msg"] = "Error al crear el registro diario"
                    return resul
            idc_diario = qsatype.FLUtil().quickSqlSelect("gt_controldiario", "idc_diario", "idusuario = '{}' AND fecha = '{}'".format(user_name, oParam["fecha"]))
            url = '/gesttare/gt_controlhorario/newRecord?p_idc_diario=' + str(idc_diario) + '&p_idusuario=' + str(user_name)
            resul["url"] = url
        else:
            resul['msg']  = "Debes indicar una fecha para crear registro de tiempo"
        return resul
        # return resul

    def gesttare_bChCursor(self, fN, cursor):
        if fN == "horasextra":
            horasordinarias = str(flgesttare_def.iface.calcula_horasordinarias_diario(cursor))
            cursor.setValueBuffer("horasordinarias", horasordinarias)
            cursor.setValueBuffer("horasordinariasstring", flgesttare_def.iface.seconds_to_time(int(horasordinarias), all_in_hours=True))

    def sumar_hora(hora1, hora2):
        formato = "%H:%M:%S"
        lista = hora2.split(":")
        hora = int(lista[0])
        minuto = int(lista[1])
        segundo = int(lista[2])
        h1 = datetime.strptime(hora1, formato)
        dh = timedelta(hours=hora)
        dm = timedelta(minutes=minuto)
        ds = timedelta(seconds=segundo)
        resultado1 = h1 + ds
        resultado2 = resultado1 + dm
        resultado = resultado2 + dh
        resultado = resultado.strftime(formato)
        return str(resultado)

    def gesttare_get_model_info(self, model, data, ident, template, where_filter):
        # print("getmodelinfo controlhorario")
        # totalhoras = 0
        # if not isinstance(data, list):
        #     return None
        # for p in data:
        #     horas = p["horasordinarias"]
        #     # lista = hora2.split(":")
        #     # hora = int(lista[0])
        #     # minuto = int(lista[1])
        #     # segundo = int(lista[2])
        #     # h1 = datetime.strptime(totalhoras, formato)
        #     # dh = timedelta(hours=hora)
        #     # dm = timedelta(minutes=minuto)
        #     # ds = timedelta(seconds=segundo)
        #     # resultado1 = h1 + ds
        #     # resultado2 = resultado1 + dm
        #     # resultado = resultado2 + dh
        #     if horas:
        #         totalhoras = totalhoras + horas
        # totalhoras = flgesttare_def.iface.seconds_to_time(int(totalhoras), all_in_hours=True)
        # return {"controldiario": "Control Diario. Tiempo total: {}".format(totalhoras)}
        return None

    def gesttare_gotoControlDiario(self, model):
        url = '/gesttare/gt_controldiario/' + str(model.idc_diario)
        return url

    def gesttare_field_completaIcon(self, model):
        if model.validado:
            return "check_box"
        else:
            return "check_box_outline_blank"

        return ""

    def gesttare_field_completaTitle(self, model):
        if model.validado:
            return "Desbloquear día"
        else:
            return "Validar día"

        return ""

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def field_usuario(self, model):
        return self.ctx.gesttare_field_usuario(model)

    def check_permissions(self, model, prefix, pk, template, acl, accion=None):
        return self.ctx.gesttare_check_permissions(model, prefix, pk, template, acl, accion)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def drawif_borrarButton(self, cursor):
        return self.ctx.gesttare_drawif_borrarButton(cursor)

    def drawif_validar(self, cursor):
        return self.ctx.gesttare_drawif_validar(cursor)

    def drawif_desbloquear(self, cursor):
        return self.ctx.gesttare_drawif_desbloquear(cursor)

    def drawif_nuevotramo(self, cursor):
        return self.ctx.gesttare_drawif_nuevotramo(cursor)

    def drawif_horasextra(self, cursor):
        return self.ctx.gesttare_drawif_horasextra(cursor)

    def validar(self, model, oParam, cursor):
        return self.ctx.gesttare_validar(model, oParam, cursor)

    def validar_dia(self, model, oParam, cursor):
        return self.ctx.gesttare_validar_dia(model, oParam, cursor)

    def borrar_dia(self, model, oParam, cursor):
        return self.ctx.gesttare_borrar_dia(model, oParam, cursor)

    def desbloquear(self, model, oParam, cursor):
        return self.ctx.gesttare_desbloquear(model, oParam, cursor)

    def gotoNuevoTramoFecha(self, model, oParam):
        return self.ctx.gesttare_gotoNuevoTramoFecha(model, oParam)

    def bChCursor(self, fN, cursor):
        return self.ctx.gesttare_bChCursor(fN, cursor)

    def get_model_info(self, model, data, ident, template, where_filter):
        return self.ctx.gesttare_get_model_info(model, data, ident, template, where_filter)

    def gotoControlDiario(self, model):
        return self.ctx.gesttare_gotoControlDiario(model)

    def field_completaIcon(self, model):
        return self.ctx.gesttare_field_completaIcon(model)

    def field_completaTitle(self, model):
        return self.ctx.gesttare_field_completaTitle(model)


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
