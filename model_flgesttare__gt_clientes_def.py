# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
from models.flgesttare import flgesttare_def


class gesttare(interna):


    def gesttare_getFilters(self, model, name, template=None):
        filters = []
        usuario = qsatype.FLUtil.nameUser()
        if name == 'clientesCompania' and usuario != "admin":
            idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
            return [{'criterio': 'idcompany__exact', 'valor': idcompany}]
        return filters

    def gesttare_iniciaValoresCursor(self, cursor=None):
        usuario = qsatype.FLUtil.nameUser()
        idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
        cursor.setValueBuffer(u"idcompany", idcompany)
        return True

    def gesttare_getClientesCompaniaUsu(self, oParam):
        usuario = qsatype.FLUtil.nameUser()
        idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_clientes")
        q.setSelect(u"idcliente, nombre, codcliente")
        q.setFrom(u"gt_clientes")
        q.setWhere(u"idcompany = '" + str(idcompany) + "' AND (UPPER(nombre) LIKE UPPER('%" + oParam["val"] + "%') OR UPPER(codcliente) LIKE UPPER('%" + oParam["val"] + "%')) ORDER BY nombre LIMIT 7")
        # q.setWhere(u"t.idtarea = '" + str(oParam['pk']) + "' AND UPPER(u.nombre) LIKE UPPER('%" + oParam["val"] + "%')  ORDER BY u.nombre LIMIT 7")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 100:
            print("sale por aqui")
            return []

        while q.next():
            # descripcion = str(q.value(2)) + "€ " + q.value(1)
            des = q.value(1)
            if q.value(2):
                des = str(des) + " #" +  str(q.value(2))
            # data.append({"idcliente": q.value(0), "nombre": des})
            data.append({"idcliente": q.value(0), "nombre": q.value(1)})
        return data

    def gesttare_getDesc(self):
        return "nombre"

    def gesttare_gotonuevoCliente(self, model, oParam):
        tengopermiso = flgesttare_def.iface.compruebaPermisosPlan("cliente")
        if tengopermiso != True:
            return tengopermiso
        # user_name = qsatype.FLUtil.nameUser()
        url='/system/gt_clientes/newRecord'
        resul = {}
        resul["url"] = url
        resul['status'] = 1
        return resul

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.gesttare_iniciaValoresCursor(cursor)

    def getClientesCompaniaUsu(self, oParam):
        return self.ctx.gesttare_getClientesCompaniaUsu(oParam)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def gotonuevoCliente(self, model, oParam):
        return self.ctx.gesttare_gotonuevoCliente(model, oParam)

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
