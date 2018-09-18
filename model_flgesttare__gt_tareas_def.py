# @class_declaration interna #
from YBLEGACY import qsatype
from YBUTILS import gesDoc


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *


class gesttare(interna):

    def gesttare_initValidation(self, name, data=None):
        response = True
        return response

    def gesttare_iniciaValoresLabel(self, model=None, template=None, cursor=None):
        labels = {}
        return labels

    def gesttare_bChLabel(self, fN=None, cursor=None):
        labels = {}
        return labels

    def gesttare_getFilters(self, model, name, template=None):
        filters = []
        return filters

    def gesttare_fun_totalDays(self, model):
        return 30

    def gesttare_getForeignFields(self, model, template=None):
        fields = [{'verbose_name': 'Proyecto', 'func': 'field_proyecto'}]
        if template == "calendarioTareas":
            return [{'verbose_name': 'totalDays', 'func': 'fun_totalDays'}]
        return fields

    def gesttare_getDesc(self):
        desc = None
        return desc

    def gesttare_actNuevoComentario(self, model, oParam):
        print("aqui insertamos comentario", oParam)
        print(u"gt_comentarios", [u"idtarea", u"fecha", u"hora", u"comentario", u"idusuario"], [model.idtarea, str(qsatype.Date())[:10], str(qsatype.Date())[-8:], oParam['comentario'], 1])
        # TODO De donde sacamos idusuario, al crear usuario en aplicacion acreamos gt_usuario?
        nombreUsuario = qsatype.FLUtil.nameUser()
        print("Usuario: ", nombreUsuario)
        idUsuario = qsatype.FLUtil.sqlSelect(u"usuarios", u"idusuario", ustr(u"idusuario = '", nombreUsuario, u"'"))
        print("idusuario: ", idUsuario)
        if not idUsuario:
            print("No existe el usuario")
            return False
        # idUsuario = "ANDRES"
        if not qsatype.FLUtil.sqlInsert(u"gt_comentarios", ["idtarea", "fecha", "hora", "comentario", "hdedicadas", "costehora", "coste", "idusuario"], [model.idtarea, str(qsatype.Date())[:10], str(qsatype.Date())[-8:], oParam['comentario'], 0, 0, 0, idUsuario]):
            print("algo salio mal?")
            return False
        return True

    def gesttare_queryGrid_calendarioTareas_initFilter(self):
        initFilter = {}
        existe = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"idtarea", ustr(u"extract(month from gt_tareas.fechavencimiento) = ", qsatype.Date().getMonth()))
        if not existe:
            return initFilter
        initFilter['where'] = u" AND extract(year from gt_tareas.fechavencimiento) = 2018"
        initFilter['where'] += u" AND extract(month from gt_tareas.fechavencimiento) = " + str(qsatype.Date().getMonth())
        initFilter['filter'] = {"s_extract(year from gt_tareas.fechavencimiento)__exact": "2018", "s_extract(month from gt_tareas.fechavencimiento)__exact": str(qsatype.Date().getMonth())}
        return initFilter

    def gesttare_queryGrid_calendarioTareas(self, model):
        query = {}
        query["tablesList"] = ("gt_tareas")
        query["select"] = ("gt_tareas.idtarea, gt_tareas.codproyecto, gt_tareas.codestado, gt_tareas.codespacio, gt_tareas.idusuario, gt_tareas.fechavencimiento, gt_tareas.descripcion, extract(day from gt_tareas.fechavencimiento) as day, extract(month from gt_tareas.fechavencimiento) as month, extract(year from gt_tareas.fechavencimiento) as year, extract(dow from date_trunc('month', gt_tareas.fechavencimiento)) as firstDay")
        # query["select"] = ("gt_tareas.idtarea, gt_tareas.fechainicio, gt_tareas.descripcion")
        query["from"] = ("gt_tareas")
        query["where"] = ("gt_tareas.fechavencimiento is not null AND 1=1")
        # query["groupby"] = " articulos.referencia, articulos.descripcion"
        # query["orderby"] = "MAX(pedidoscli.fecha) DESC"
        return query

    def gesttare_getListaTarea(self, model, oParam):
        print("________________________")
        print(oParam)
        return []
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"articulos")
        q.setSelect(u"referencia,descripcion")
        q.setFrom(u"articulos")
        q.setWhere(u"UPPER(referencia) LIKE '%" + oParam['val'].upper() + "%' OR UPPER(descripcion) LIKE '%" + oParam['val'].upper() + "%' AND sevende = true")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 200:
            return []

        while q.next():
            descripcion = str(q.value(0)) + "  " + q.value(1)
            data.append({"descripcion": descripcion, "referencia": q.value(0)})

        return data

    def gesttare_cambiarFecha(self, model, oParam, cursor):
        nuevaFecha = oParam["fechavencimiento"]
        print("cambiar fecha ", nuevaFecha)
        if nuevaFecha:
            cursor.setValueBuffer("fechavencimiento", nuevaFecha)
            if not cursor.commitBuffer():
                return False
        return True

    def gesttare_field_proyecto(self, model):
        nombreProy = ""
        if not model.codproyecto:
            return nombreProy
        nombreProy = model.codproyecto.nombre
        return nombreProy

    def gesttare_uploadFile(self, model, oParam):
        print("aqui insertamos comentario", oParam)
        # print(u"gt_comentarios", [u"idtarea", u"fecha", u"hora", u"comentario", u"idusuario"], [model.idtarea, str(qsatype.Date())[:10], str(qsatype.Date())[-8:], oParam['comentario'], 1])
        # TODO De donde sacamos idusuario, al crear usuario en aplicacion acreamos gt_usuario?
        nombreUsuario = qsatype.FLUtil.nameUser()
        print("Usuario: ", nombreUsuario)
        idUsuario = qsatype.FLUtil.sqlSelect(u"usuarios", u"idusuario", ustr(u"idusuario = '", nombreUsuario, u"'"))
        print("idusuario: ", idUsuario)
        if not idUsuario:
            print("No existe el usuario")
            return False
        # idUsuario = "ANDRES"
        # if not qsatype.FLUtil.sqlInsert(u"gt_comentarios", ["idtarea", "fecha", "hora", "comentario", "hdedicadas", "costehora", "coste", "idusuario"], [model.idtarea, str(qsatype.Date())[:10], str(qsatype.Date())[-8:], oParam['comentario'], 0, 0, 0, idUsuario]):
        #     print("algo salio mal?")
        #     return False
        cursor = qsatype.FLSqlCursor(u"gt_comentarios")
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"idtarea", model.idtarea)
        cursor.setValueBuffer(u"fecha", str(qsatype.Date())[:10])
        cursor.setValueBuffer(u"hora", str(qsatype.Date())[-8:])
        cursor.setValueBuffer(u"comentario", oParam['comentario'])
        cursor.setValueBuffer(u"hdedicadas", 0)
        cursor.setValueBuffer(u"costehora", 0)
        cursor.setValueBuffer(u"coste", 0)
        cursor.setValueBuffer(u"idusuario", idUsuario)
        if not cursor.commitBuffer():
            print("algo salio mal")
            return False
        print("_____________")
        print(cursor.setValueBuffer("idcomentario"))
        if not gesDoc.fileUpload("gt_comentarios", cursor.setValueBuffer("idcomentario"), oParam['fileData']):
            return False
        return True

    def __init__(self, context=None):
        super(gesttare, self).__init__(context)

    def initValidation(self, name, data=None):
        return self.ctx.gesttare_initValidation(name, data=None)

    def iniciaValoresLabel(self, model=None, template=None, cursor=None):
        return self.ctx.gesttare_iniciaValoresLabel(model, template, cursor)

    def bChLabel(self, fN=None, cursor=None):
        return self.ctx.gesttare_bChLabel(fN, cursor)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def actNuevoComentario(self, model, oParam):
        return self.ctx.gesttare_actNuevoComentario(model, oParam)

    def queryGrid_calendarioTareas(self, model):
        return self.ctx.gesttare_queryGrid_calendarioTareas(model)

    def getListaTarea(self, model, oParam):
        return self.ctx.gesttare_getListaTarea(model, oParam)

    def cambiarFecha(self, model, oParam, cursor):
        return self.ctx.gesttare_cambiarFecha(model, oParam, cursor)

    def fun_totalDays(self, model):
        return self.ctx.gesttare_fun_totalDays(model)

    def fun_firstDay(self, model):
        return self.ctx.gesttare_fun_firstDay(model)

    def queryGrid_calendarioTareas_initFilter(self):
        return self.ctx.gesttare_queryGrid_calendarioTareas_initFilter()

    def field_proyecto(self, model):
        return self.ctx.gesttare_field_proyecto(model)

    def uploadFile(self, model, oParam):
        return self.ctx.gesttare_uploadFile(model, oParam)


# @class_declaration head #
class head(gesttare):

    def __init__(self, context=None):
        super(head, self).__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super(ifaceCtx, self).__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
