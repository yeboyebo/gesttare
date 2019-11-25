# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *


class gesttare(interna):

    def gesttare_getDesc(self):
        return "nombre"

    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        fields = [
            {'verbose_name': 'Color responsable', 'func': 'color_responsable'},
            {'verbose_name': 'Responsable', 'func': 'field_usuario'},
            {'verbose_name': 'porcentaje', 'func': 'fun_porcentaje'},
            {'verbose_name': 'ntareas', 'func': 'fun_ntareas'}
        ]
        return fields

    def gesttare_field_usuario(self, model):
        nombre_usuario = ""
        # if hasattr(model.idresponsable, 'usuario'):
        #     print("el valor es: ",model.idresponsable.usuario)
        try:
            if not model.idusuario:
                return nombre_usuario
            nombre_usuario = "@" + model.idusuario.usuario
        except Exception:
            pass
        return nombre_usuario

        return fields

    def gesttare_color_responsable(self, model):
        if hasattr(model.idusuario, 'idusuario'):
            return "responsable"

        return ""

    def gesttare_fun_porcentaje(self, model):
        return 50

    def gesttare_fun_ntareas(self, model):
        ntareas = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"count(idtarea)", ustr(u"idhito = '", str(model.idhito), u"'")) or 0
        return ntareas

    def gesttare_iniciaValoresCursor(self, cursor=None):
        usuario = qsatype.FLUtil.nameUser()
        # idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
        # cursor.setValueBuffer(u"idcompany", idcompany)
        cursor.setValueBuffer("idusuario", usuario)

        if cursor.valueBuffer("nombre") == None:
            cursor.setValueBuffer("nombre", "Coordinación")

        qsatype.FactoriaModulos.get('formRecordgt_hitosproyecto').iface.iniciaValoresCursor(cursor)
        return True

    def gesttare_getHitosProyecto(self, oParam):
        data = []
        if "codproyecto" not in oParam:
            return data
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_proyectos, gt_hitosproyecto")
        q.setSelect(u"h.idhito, h.nombre")
        q.setFrom(u"gt_proyectos p INNER JOIN gt_hitosproyecto h ON p.codproyecto = h.codproyecto")
        q.setWhere(u"p.codproyecto = '" + str(oParam['codproyecto']) + "' AND (UPPER(h.nombre) LIKE UPPER('%" + oParam["val"] + "%')) AND h.resuelta = false  ORDER BY h.nombre LIMIT 8")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 100:
            print("sale por aqui")
            return []

        while q.next():
            # descripcion = str(q.value(2)) + "€ " + q.value(1)
            data.append({"idhito": q.value(0), "nombre": q.value(1)})
        return data

    def __init__(self, context=None):
        super().__init__(context)

    def getHitosProyecto(self, oParam):
        return self.ctx.gesttare_getHitosProyecto(oParam)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def field_usuario(self, model):
        return self.ctx.gesttare_field_usuario(model)

    def color_responsable(self, model):
        return self.ctx.gesttare_color_responsable(model)

    def fun_porcentaje(self, model):
        return self.ctx.gesttare_fun_porcentaje(model)

    def fun_ntareas(self, model):
        return self.ctx.gesttare_fun_ntareas(model)

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.gesttare_iniciaValoresCursor(cursor)


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
