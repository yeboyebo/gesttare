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
        return None

    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        if template == "notificacionesUsuario":
            return [{'verbose_name': 'nombreUsuario', 'func': 'field_nombreUsuario'}]

        return fields

    def gesttare_field_nombreUsuario(self, model):
        nombre_usuario = ""
        try:
            print(model['gt_actualizaciones.idusuarioorigen'])
            nombre_usuario = qsatype.FLUtil.sqlSelect(u"usuarios", u"nombre", ustr(u"idusuario = '", model['gt_actualizaciones.idusuarioorigen'], "'"))
        except Exception:
            pass
        return nombre_usuario

    def gesttare_queryGrid_notificacionesUsuario(self, model):
        idUsuario = qsatype.FLUtil.nameUser()
        query = {}
        query["tablesList"] = ("gt_actualizusuario,gt_actualizaciones,usuarios")
        query["select"] = ("gt_actualizaciones.idactualizacion, gt_actualizusuario.idactualizusuario, gt_actualizaciones.idtarea, gt_actualizaciones.tipo,gt_actualizaciones.idcomentario,gt_actualizaciones.fecha,gt_actualizaciones.hora,gt_actualizusuario.idusuario,gt_tareas.nombre, gt_actualizaciones.idusuarioorigen")
        query["from"] = ("gt_actualizusuario INNER JOIN gt_actualizaciones ON gt_actualizusuario.idactualizacion = gt_actualizaciones.idactualizacion INNER JOIN usuarios ON gt_actualizusuario.idusuario = usuarios.idusuario INNER JOIN gt_tareas ON gt_tareas.idtarea = gt_actualizaciones.idtarea")
        query["where"] = ("gt_actualizusuario.idusuario = '" + idUsuario + "'")
        return query

    def gesttare_visualizarTarea(self, model):
        print("_______")
        print(model.idtarea.idtarea)
        idtarea = model.idtarea.idtarea
        print(idtarea)
        # porlotes = articulos.objects.filter(referencia__exact=model.referencia.referencia)
        # print(porlotes)
        # if porlotes[0].porlotes:
        return '/gesttare/gt_tareas/' + str(idtarea)

    def gesttare_borrarActualizacion(self, model, oParam):
        print("borrando actualizacion")
        idactualizacion = model.idactualizacion
        print(idactualizacion)
        # print(ustr(u"DELETE FROM gt_actualizaciones WHERE idactualizacion = '", idactualizacion, "'"))
        if not qsatype.FLUtil.sqlDelete(u"gt_actualizusuario",ustr(u"idactualizacion = ", idactualizacion)):
            # print("falla la query")
            # return False
        # if not qsatype.FLUtil.sqlDelete(u"gt_actualizaciones", ustr(u"idactualizacion = ", idactualizacion)):
            print("sale por false")
            return False
        print("sale por true")
        return True

    def __init__(self, context=None):
        super().__init__(context)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def field_nombreUsuario(self, model):
        return self.ctx.gesttare_field_nombreUsuario(model)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def queryGrid_notificacionesUsuario(self, model):
        return self.ctx.gesttare_queryGrid_notificacionesUsuario(model)

    def visualizarTarea(self, model):
        return self.ctx.gesttare_visualizarTarea(model)

    def borrarActualizacion(self, model, oParam):
        return self.ctx.gesttare_borrarActualizacion(model, oParam)


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
