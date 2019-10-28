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
            nombre_usuario = qsatype.FLUtil.sqlSelect(u"aqn_user", u"nombre", ustr(u"idusuario = '", model['gt_actualizaciones.idusuarioorigen'], "'"))
        except Exception:
            pass
        return nombre_usuario

    def gesttare_queryGrid_notificacionesUsuario(self, model):
        idUsuario = qsatype.FLUtil.nameUser()
        query = {}
        query["tablesList"] = ("gt_actualizusuario,gt_actualizaciones,aqn_user")
        query["select"] = ("gt_actualizaciones.idactualizacion, gt_actualizusuario.idactualizusuario, gt_actualizaciones.otros, gt_actualizaciones.idtarea, gt_actualizaciones.tipo,gt_actualizaciones.idcomentario,gt_actualizaciones.fecha,gt_actualizaciones.hora,gt_actualizusuario.idusuario,gt_tareas.nombre, gt_actualizaciones.idusuarioorigen")
        query["from"] = ("gt_actualizusuario INNER JOIN gt_actualizaciones ON gt_actualizusuario.idactualizacion = gt_actualizaciones.idactualizacion INNER JOIN aqn_user ON gt_actualizusuario.idusuario = aqn_user.idusuario LEFT JOIN gt_tareas ON gt_tareas.idtarea = gt_actualizaciones.idtarea")
        query["where"] = ("gt_actualizusuario.idusuario = '" + idUsuario + "' AND (gt_actualizaciones.idusuarioorigen <> '" + idUsuario + "' OR (gt_actualizaciones.idusuarioorigen = '" + idUsuario + "' AND gt_actualizaciones.tipo = 'anotacion'))")
        return query

    def gesttare_visualizarElemento(self, model, cursor):
        response = {}
        print("___________")
        print(cursor.valueBuffer("tipobjeto"))
        if cursor.valueBuffer("tipo") == "anotacion":
            response["status"] = 2
            response["confirm"] = cursor.valueBuffer("otros") + "</br>" + cursor.valueBuffer("tipobjeto")
            # print(response)
            return response
            # return '/gesttare/gt_actualizaciones/' + str(cursor.valueBuffer("idactualizacion"))
        elif cursor.valueBuffer("tipobjeto") == "proyecto":
            response["url"] = '/gesttare/gt_tareas/' + str(cursor.valueBuffer("idobjeto"))
            return response
        elif cursor.valueBuffer("tipobjeto") == "gt_comentario":
            idtarea = qsatype.FLUtil().quickSqlSelect("gt_comentarios", "idtarea", "idcomentario = '{}'".format(cursor.valueBuffer("idobjeto")))
            response["url"] = '/gesttare/gt_tareas/' + str(idtarea)
            return response
        print(model.idtarea.idtarea)
        idtarea = model.idtarea.idtarea
        print(idtarea)
        # porlotes = articulos.objects.filter(referencia__exact=model.referencia.referencia)
        # print(porlotes)
        # if porlotes[0].porlotes:
        response["url"] = '/gesttare/gt_tareas/' + str(idtarea)
        return response

    def gesttare_borrarActualizacion(self, model, oParam):
        idactualizacion = model.idactualizacion
        idUsuario = qsatype.FLUtil.nameUser()
        resul = {}
        # print(ustr(u"DELETE FROM gt_actualizaciones WHERE idactualizacion = '", idactualizacion, "'"))
        if not qsatype.FLUtil.sqlDelete(u"gt_actualizusuario",ustr(u"idactualizacion = ", idactualizacion, " AND idusuario = ", idUsuario)):
            # print("falla la query")
            # return False
        # if not qsatype.FLUtil.sqlDelete(u"gt_actualizaciones", ustr(u"idactualizacion = ", idactualizacion)):
            #return False
            resul["status"] = 1
            resul["msg"] = "Error en la eliminación de la actualización"
        resul["return_data"] = True
        resul["msg"] = "Notificación eliminada correctamente"
        return resul

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

    def visualizarElemento(self, model, cursor):
        return self.ctx.gesttare_visualizarElemento(model, cursor)

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
