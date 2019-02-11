# @class_declaration interna #
import json

from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *


class gesttare(interna):

    def gesttare_getDesc(self):
        desc = "nombre"
        return desc

    def gesttare_actNuevoPartic(self, oParam, cursor):
        response = {}
        if "partic" not in oParam:
            # idUsuario = cursor.valueBuffer("idusuario")
            qryUsuarios = qsatype.FLSqlQuery()
            qryUsuarios.setTablesList(u"usuarios")
            qryUsuarios.setSelect(u"idusuario, nombre")
            qryUsuarios.setFrom(ustr(u"usuarios"))
            # qryUsuarios.setWhere(ustr(u"idusuario <> '", idUsuario, u"'"))
            qryUsuarios.setWhere(ustr(u"1 = 1"))
            if not qryUsuarios.exec_():
                return False

            opts = []
            while qryUsuarios.next():
                tengousuario = qsatype.FLUtil.sqlSelect("gt_particproyecto", "idusuario", "idusuario = '{}' AND codproyecto = '{}'".format(qryUsuarios.value("idusuario"), cursor.valueBuffer("codproyecto")))
                value = False
                if tengousuario:
                    value = True

                opts.append({"key": qryUsuarios.value("idusuario"), "label": qryUsuarios.value("nombre"), "value": value})

            response['status'] = -1
            response['data'] = {}
            response['params'] = [
                {
                    "componente": "YBFieldDB",
                    "prefix": "gt_proyectos",
                    "style": {
                        "width": "100%"
                    },
                    "tipo": 180,
                    "verbose_name": "Participantes",
                    "label": "Participantes",
                    "key": "partic",
                    "validaciones": None,
                    "required": False,
                    "opts": opts
                }
            ]
            return response
        else:
            participantes = json.loads(oParam["partic"])
            for p in participantes:
                curPartic = qsatype.FLSqlCursor("gt_particproyecto")
                curPartic.select("idusuario = '{}' AND codproyecto = '{}'".format(p, cursor.valueBuffer("codproyecto")))
                curPartic.refreshBuffer()

                if curPartic.first():
                    if participantes[p] is False:
                        # print("vamos a borrar")
                        curPartic.setModeAccess(cursor.Del)
                        curPartic.refreshBuffer()
                        if not curPartic.commitBuffer():
                            return False
                else:
                    if participantes[p] is True:
                        # print("vamos a crear")
                        curPartic.setModeAccess(curPartic.Insert)
                        curPartic.refreshBuffer()
                        curPartic.setValueBuffer("idusuario", p)
                        curPartic.setValueBuffer("codproyecto", cursor.valueBuffer("codproyecto"))
                        if not curPartic.commitBuffer():
                            return False

            return True

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def actNuevoPartic(self, oParam, cursor):
        return self.ctx.gesttare_actNuevoPartic(oParam, cursor)


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
