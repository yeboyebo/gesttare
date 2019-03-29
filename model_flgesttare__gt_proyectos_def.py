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
        if "idusuario" not in oParam:
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
                    "prefix": "otros",
                    "rel": "usuarios",
                    "style": {
                        "width": "100%"
                    },
                    "tipo": 180,
                    "verbose_name": "Participantes",
                    "label": "Participantes",
                    "key": "idusuario",
                    "desc": "nombre",
                    "validaciones": None,
                    "required": False,
                    "opts": opts
                }
            ]
            return response
        else:
            participantes = json.loads(oParam["idusuario"])
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

    def gesttare_getFilters(self, model, name, template=None):
        filters = []
        if name == 'proyectosusuario':
            # proin = "("
            proin = []
            usuario = qsatype.FLUtil.nameUser()
            curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
            curProyectos.select("idusuario = '" + str(usuario) + "'")
            while curProyectos.next():
                curProyectos.setModeAccess(curProyectos.Browse)
                curProyectos.refreshBuffer()
                proin.append(curProyectos.valueBuffer("codproyecto"))
                # proin = proin + "'" + curProyectos.valueBuffer("codproyecto") + "', "
            # proin = proin + " null)"
            return [{'criterio': 'codproyecto__in', 'valor': proin, 'tipo': 'q'}]
        return filters

    def gesttare_check_permissions(self, model, prefix, pk, template, acl, accion):
        if template == "formRecord":
            nombreUsuario = qsatype.FLUtil.nameUser()
            pertenece = qsatype.FLUtil.sqlSelect(u"gt_particproyecto", u"idusuario", ustr(u"idusuario = '", nombreUsuario, u"' AND codproyecto = '", pk, "'"))
            if not pertenece:
                return False
        return True

    def gesttare_getProyectosUsuario(self, oParam):
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_proyectos, gt_particproyecto")
        q.setSelect(u"p.codproyecto, t.nombre")
        q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.codproyecto=p.codproyecto")
        q.setWhere(u"p.idusuario = '" + qsatype.FLUtil.nameUser() + "' AND UPPER(t.nombre) like UPPER('%" + oParam["val"] + "%')  ORDER BY t.nombre LIMIT 7")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 100:
            print("sale por aqui")
            return []

        while q.next():
            # descripcion = str(q.value(2)) + "€ " + q.value(1)
            data.append({"codproyecto": q.value(0), "nombre": q.value(1)})

        return data

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def actNuevoPartic(self, oParam, cursor):
        return self.ctx.gesttare_actNuevoPartic(oParam, cursor)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def check_permissions(self, model, prefix, pk, template, acl, accion=None):
        return self.ctx.gesttare_check_permissions(model, prefix, pk, template, acl, accion)

    def getProyectosUsuario(self, oParam):
        return self.ctx.gesttare_getProyectosUsuario(oParam)


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
