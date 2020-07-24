# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
import json


class gesttare(interna):

    def gesttare_getDesc(self):
        return None

    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        if template == "notificacionesUsuario" or template == "notificacionesUsuarioViejas":
            return [{'verbose_name': 'actIcon', 'func': 'field_actIcon'}, {'verbose_name': 'nombreUsuario', 'func': 'field_nombreUsuario'}, {'verbose_name': 'verConvertirTarea', 'func': 'field_verConvertirTarea'}, {'verbose_name': 'verTranspasarAnotacion', 'func': 'field_verTranspasarAnotacion'}, {'verbose_name': 'Color_responsable', 'func': 'field_color_responsable'}, {'verbose_name': 'Color_fondo_icono', 'func': 'field_color_fondo_icono'},{'verbose_name': 'titulo_icono', 'func': 'field_titulo_icono'} ]

        return fields

    def gesttare_field_nombreUsuario(self, model):
        nombre_usuario = ""
        try:
            nombre_usuario = qsatype.FLUtil.sqlSelect(u"aqn_user", u"usuario", ustr(u"idusuario = '", model['gt_actualizaciones.idusuarioorigen'], "'"))
            nombre_usuario = "@" + nombre_usuario
        except Exception:
            pass
        return nombre_usuario

    def gesttare_field_verConvertirTarea(sefl, model):
        if model["gt_actualizaciones.tipo"] != "anotacion" and model["gt_actualizaciones.tipo"] != "inbox":
            return "hidden"
        else:
            return ""

    def gesttare_field_verTranspasarAnotacion(sefl, model):
        if model["gt_actualizaciones.tipo"] != "anotacion" and model["gt_actualizaciones.tipo"] != "inbox":
            return "hidden"
        else:
            return ""

    def gesttare_field_color_responsable(self, model):
        return "responsable"

    def gesttare_field_color_fondo_icono(self, model):
        retorno = ""
        if model["gt_actualizaciones.tipo"]:
            if model["gt_actualizaciones.tipo"] == "resuelta":
                retorno = "verdeAnotar"
            elif model["gt_actualizaciones.tipo"] == "abierta":
                retorno = "amarilloAnotar"
            elif model["gt_actualizaciones.tipo"] == "cambioFechaEjecucion":
                retorno = "naranjaAnotar"
            elif model["gt_actualizaciones.tipo"] == "comentario":
                retorno = "lilaAnotar"
            elif model["gt_actualizaciones.tipo"] == "partictarea" or model["gt_actualizaciones.tipo"] == "particproyecto":
                retorno = "amarilloAnotar"
            elif model["gt_actualizaciones.tipo"] == "responsable" or model["gt_actualizaciones.tipo"] == "responsablepro":
                retorno = "marronAnotar"
            elif model["gt_actualizaciones.tipo"] == "delpartictarea" or model["gt_actualizaciones.tipo"] == "delparticproyecto":
                retorno = "rojoAnotar"
            elif model["gt_actualizaciones.tipo"] == "deltarea":
                retorno = "rojoAnotar"
            elif model["gt_actualizaciones.tipo"] == "anotacion" or model["gt_actualizaciones.tipo"] == "inbox":
                retorno = "verdeazulAnotar"
            elif model["gt_actualizaciones.tipo"] == "archivado":
                retorno = "aquaAnotar"
            elif model["gt_actualizaciones.tipo"] == "desarchivado":
                retorno = "aquaAnotar"
            elif model["gt_actualizaciones.tipo"] == "colaborador":
                retorno = "aquaAnotar"
            elif model["gt_actualizaciones.tipo"] == "observador":
                retorno = "aquaAnotar"

        return retorno

    def gesttare_field_actIcon(self, model):
        # return "accessible"
        retorno = ""
        if model["gt_actualizaciones.tipo"]:
            if model["gt_actualizaciones.tipo"] == "resuelta":
                retorno = "/static/dist/img/icons/check_box.svg"
            elif model["gt_actualizaciones.tipo"] == "abierta":
                retorno = "/static/dist/img/icons/check_box_outline_blank.svg"
            elif model["gt_actualizaciones.tipo"] == "cambioFechaEjecucion":
                retorno = "/static/dist/img/icons/update.svg"
            elif model["gt_actualizaciones.tipo"] == "comentario":
                retorno = "/static/dist/img/icons/chat.svg"
            elif model["gt_actualizaciones.tipo"] == "partictarea" or model["gt_actualizaciones.tipo"] == "particproyecto":
                retorno = "/static/dist/img/icons/group_add.svg"
            elif model["gt_actualizaciones.tipo"] == "responsable" or model["gt_actualizaciones.tipo"] == "responsablepro":
                retorno = "/static/dist/img/icons/supervisor_account.svg"
            elif model["gt_actualizaciones.tipo"] == "delpartictarea" or model["gt_actualizaciones.tipo"] == "delparticproyecto":
                retorno = "/static/dist/img/icons/eliminadoParticipante.svg"
            elif model["gt_actualizaciones.tipo"] == "deltarea":
                retorno = "/static/dist/img/icons/delete.svg"
            elif model["gt_actualizaciones.tipo"] == "anotacion":
                retorno = "/static/dist/img/icons/note.svg"
            elif model["gt_actualizaciones.tipo"] == "inbox":
                retorno = "/static/dist/img/icons/envelope.svg"
            elif model["gt_actualizaciones.tipo"] == "archivado":
                retorno = "/static/dist/img/icons/archive.svg"
            elif model["gt_actualizaciones.tipo"] == "desarchivado":
                retorno = "/static/dist/img/icons/unarchive.svg"
            elif model["gt_actualizaciones.tipo"] == "colaborador":
                retorno = "/static/dist/img/icons/colaborador.svg"
            elif model["gt_actualizaciones.tipo"] == "observador":
                retorno = "/static/dist/img/icons/observador_blanco.svg"

        return retorno


    def gesttare_field_titulo_icono(self, model):
        # print(model["gt_actualizaciones.tipo"])
        retorno = ""
        if model["gt_actualizaciones.tipo"]:
            if model["gt_actualizaciones.tipo"] == "resuelta":
                retorno = "Tarea Completada"
            elif model["gt_actualizaciones.tipo"] == "abierta":
                retorno = "Tarea abierta"
            elif model["gt_actualizaciones.tipo"] == "cambioFechaEjecucion":
                retorno = "Cambio fecha ejecución"
            elif model["gt_actualizaciones.tipo"] == "comentario":
                retorno = "Comentario"
            elif model["gt_actualizaciones.tipo"] == "partictarea" or model["gt_actualizaciones.tipo"] == "particproyecto":
                retorno = "Añadido como participante"
            elif model["gt_actualizaciones.tipo"] == "responsable" or model["gt_actualizaciones.tipo"] == "responsablepro":
                retorno = "Asignado como responsable"
            elif model["gt_actualizaciones.tipo"] == "delpartictarea" or model["gt_actualizaciones.tipo"] == "delparticproyecto":
                retorno = "Eliminado como participante"
            elif model["gt_actualizaciones.tipo"] == "deltarea":
                retorno = "Eliminado"
            elif model["gt_actualizaciones.tipo"] == "anotacion":
                retorno = "Posible tarea"
            elif model["gt_actualizaciones.tipo"] == "inbox":
                retorno = "Posible tarea"
            elif model["gt_actualizaciones.tipo"] == "archivado":
                retorno = "Proyecto archivado"
            elif model["gt_actualizaciones.tipo"] == "desarchivado":
                retorno = "Proyecto desarchivado"
            elif model["gt_actualizaciones.tipo"] == "colaborador":
                retorno = "Invitación a proyecto para colaborar"
            elif model["gt_actualizaciones.tipo"] == "observador":
                retorno = "Invitación a proyecto para observar"

        return retorno
    

    def gesttare_queryGrid_notificacionesUsuario(self, model):
        idUsuario = qsatype.FLUtil.nameUser()
        query = {}
        query["tablesList"] = ("gt_actualizusuario,gt_actualizaciones,aqn_user")
        query["select"] = ("gt_actualizaciones.idactualizacion, gt_actualizusuario.idactualizusuario, gt_actualizaciones.otros, gt_actualizaciones.idtarea, gt_actualizaciones.tipo,gt_actualizaciones.idcomentario,gt_actualizaciones.fecha,gt_actualizaciones.hora,gt_actualizusuario.idusuario,gt_tareas.nombre, gt_actualizaciones.idusuarioorigen")
        query["from"] = ("gt_actualizusuario INNER JOIN gt_actualizaciones ON gt_actualizusuario.idactualizacion = gt_actualizaciones.idactualizacion INNER JOIN aqn_user ON gt_actualizusuario.idusuario = aqn_user.idusuario LEFT JOIN gt_tareas ON gt_tareas.idtarea = gt_actualizaciones.idtarea")
        query["where"] = ("gt_actualizusuario.idusuario = '" + idUsuario + "' AND (gt_actualizaciones.idusuarioorigen <> '" + idUsuario + "' OR (gt_actualizaciones.idusuarioorigen = '" + idUsuario + "' AND (gt_actualizaciones.tipo = 'anotacion' OR gt_actualizaciones.tipo = 'inbox'))) AND gt_actualizaciones.fecha BETWEEN '2019-11-16' AND '2500-12-20'")
        query["orderby"] = "gt_actualizaciones.fecha DESC, gt_actualizaciones.hora DESC"
        return query

    def gesttare_queryGrid_notificacionesUsuarioViejas(self, model):
        idUsuario = qsatype.FLUtil.nameUser()
        query = {}
        query["tablesList"] = ("gt_actualizusuario,gt_actualizaciones,aqn_user")
        query["select"] = ("gt_actualizaciones.idactualizacion, gt_actualizusuario.idactualizusuario, gt_actualizaciones.otros, gt_actualizaciones.idtarea, gt_actualizaciones.tipo,gt_actualizaciones.idcomentario,gt_actualizaciones.fecha,gt_actualizaciones.hora,gt_actualizusuario.idusuario,gt_tareas.nombre, gt_actualizaciones.idusuarioorigen")
        query["from"] = ("gt_actualizusuario INNER JOIN gt_actualizaciones ON gt_actualizusuario.idactualizacion = gt_actualizaciones.idactualizacion INNER JOIN aqn_user ON gt_actualizusuario.idusuario = aqn_user.idusuario LEFT JOIN gt_tareas ON gt_tareas.idtarea = gt_actualizaciones.idtarea")
        query["where"] = ("gt_actualizusuario.idusuario = '" + idUsuario + "' AND (gt_actualizaciones.idusuarioorigen <> '" + idUsuario + "'AND gt_actualizaciones.fecha BETWEEN '2010-11-10' AND '2019-11-18') ")
        return query

    def gesttare_visualizarElemento(self, model, cursor):
        response = {}
        if cursor.valueBuffer("tipo") == "deltarea":
            response["msg"] = "Tarea eliminada"
            return response
        elif cursor.valueBuffer("tipo") == "delproyecto":
            response["msg"] = "Proyecto eliminado"
            return response
        if cursor.valueBuffer("tipo") == "anotacion" or cursor.valueBuffer("tipo") == "inbox":
            response["status"] = 2
            response["confirm"] = "<div class='anotacionNombre'>Nombre: </div><div class='anotacionNombreOtros'>" + cursor.valueBuffer("otros") + "</div></br>" + "<div class='anotacionDescripcion'>Descripción: </div><div class='anotacionDescripcionTipobjeto'>" + cursor.valueBuffer("tipobjeto") + "</div>"
            if cursor.valueBuffer("tipo") == "inbox":
                clave = qsatype.FLUtil.sqlSelect("gd_objetosdoc", "clave", "clave = '{}'".format(cursor.valueBuffer("idactualizacion")))
                if clave:
                    documentos = ""
                    q = qsatype.FLSqlQuery()
                    q.setTablesList(u"gd_objetosdoc, gd_documentos")
                    q.setSelect("gd_documentos.nombre")
                    q.setFrom("gd_objetosdoc INNER JOIN gd_documentos ON gd_objetosdoc.iddocumento = gd_documentos.iddocumento")
                    q.setWhere(u"gd_objetosdoc.clave = '" + str(cursor.valueBuffer("idactualizacion")) + "'")

                    if not q.exec_():
                        print("Error inesperado")
                        return []
                    if q.size() > 200:
                        return []

                    while q.next():
                        documentos += "<li>" + str(q.value(0)) + " </li> "
                    response["confirm"] += "</br><div class='anotacionDescripcion'>Adjuntos: </div><div class='anotacionDescripcionTipobjeto'>" + documentos + "</div>"
            response["customButtons"] = []
       
        elif cursor.valueBuffer("tipobjeto") in ["proyecto", "gt_proyecto"]:
            response["url"] = '/gesttare/gt_proyectos/' + str(cursor.valueBuffer("idobjeto"))
            return response
        # elif cursor.valueBuffer("tipobjeto") == "gt_comentario":
        #     idtarea = qsatype.FLUtil().quickSqlSelect("gt_comentarios", "idtarea", "idcomentario = '{}'".format(cursor.valueBuffer("idobjeto")))
        #     response["url"] = '/gesttare/gt_tareas/' + str(idtarea)
        #     return response
        if model.idtarea:
            idtarea = model.idtarea.idtarea
            # porlotes = articulos.objects.filter(referencia__exact=model.referencia.referencia)
            # print(porlotes)
            # if porlotes[0].porlotes:
            response["url"] = '/gesttare/gt_tareas/' + str(idtarea)
        else:
            response["url"] = '/gesttare/gt_tareas/' + str(cursor.valueBuffer("idobjeto"))

        if cursor.valueBuffer("tipo") == "colaborador" or cursor.valueBuffer("tipo") == "observador":
            if cursor.valueBuffer("tipo") == "colaborador":
                tipo_participa = "colaborar"
            else:
                tipo_participa = "observar"
            id_compania = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(cursor.valueBuffer("idusuarioorigen")))
            nombre_compania = qsatype.FLUtil.sqlSelect("aqn_companies", "descripcion", "idcompany = '{}'".format(id_compania))
            response["status"] = -1
            response['data'] = {}
            response["prefix"] = "gt_actualizaciones"
            response["title"] = "<div class = 'modalExterno'>Has recibido una invitación para <strong>" + tipo_participa + "</strong> en el proyecto <strong>" + cursor.valueBuffer("otros") + "</strong> de la compañía <strong>" + nombre_compania + "</strong></div"
            # response["title"] = "<div>algo</div>"

            response["serverAction"] = "aceptarColaborador"
            response["customButtons"] = [{"accion": "serverAction", "pk": cursor.valueBuffer("idactualizacion"), "nombre": "Aceptar invitación", "serverAction": "aceptarColaborador", "className": "creaAnotacionButton"}]
            response["params"] = []


        return response

    def gesttare_aceptarColaborador(self, oParam, cursor):
        usuario = qsatype.FLUtil.nameUser()
        response = {}
        cursor_paricipo = qsatype.FLSqlCursor(u"gt_particproyecto")
        cursor_paricipo.setModeAccess(cursor_paricipo.Insert)
        cursor_paricipo.refreshBuffer()
        cursor_paricipo.setValueBuffer(u"idusuario", usuario)
        cursor_paricipo.setValueBuffer(u"idproyecto", cursor.valueBuffer("idobjeto"))
        cursor_paricipo.setValueBuffer(u"tipo", cursor.valueBuffer("tipo"))
       
        if not cursor_paricipo.commitBuffer():
            return False

        if not qsatype.FLUtil.sqlDelete(u"gt_actualizusuario",ustr(u"idactualizacion = ", cursor.valueBuffer("idactualizacion"), " AND idusuario = " + usuario)):
            print("error")
            return False
       
        # response["resul"] = True
        # response["msg"] = "Invitación aceptada"
        response["url"] = '/gesttare/gt_proyectos/' + str(cursor.valueBuffer("idobjeto"))
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

    def gesttare_convertirTarea(self, model, oParam):
        # Como controlamos si luego no crea la tarea??
        qsatype.FLSqlQuery().execSql("DELETE FROM gt_actualizusuario where idactualizacion = '" + str(model.idactualizacion) + "'")
        response = {}
        # descripcion = str(model.tipobjeto)
        # descripcion.replace('\n', "")
        # descripcion.replace('\r', "")
        # descripcion.replace('\t', "")
        # descripcion.replace('<', "")
        # response["url"] = '/gesttare/gt_tareas/newRecord?p_nombre='+ str(model.otros) + "&p_descripcion=" + descripcion
        # response["url"] = '/gesttare/gt_tareas/newRecord?p_nombre='+ "gt_ac_" + str(model.idactualizacion)
        response["url"] = '/gesttare/gt_tareas/newRecord?p_idactualizacion=' + str(model.idactualizacion)
        return response

    def gesttare_transpasarAnotacion(self, model, oParam):
        response = {}
        if "idusuario" not in oParam:
            response['status'] = -1
            response['data'] = {}
            response['params'] = [
                {
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "rel": "aqn_user",
                    "style": {
                        "width": "100%"
                    },
                    "tipo": 185,
                    "verbose_name": "Participantes",
                    "label": "Participantes",
                    "function": "getParticCompaniaUsu",
                    "key": "idusuario",
                    "desc": "usuario",
                    "validaciones": None,
                    "required": False
                }
            ]
            return response
        else:
            participantes = json.loads(oParam["idusuario"])
            for p in participantes:
                if participantes[p] is True:
                    qsatype.FLSqlQuery().execSql("DELETE FROM gt_actualizusuario where idactualizacion = '" + str(model.idactualizacion) + "'")
                    if not qsatype.FLUtil.sqlInsert(u"gt_actualizusuario", qsatype.Array([u"idactualizacion", u"idusuario", u"revisada"]), qsatype.Array([model.idactualizacion, p, False])):
                        return False
            response = {}
            response["resul"] = True
            response["msg"] = "Posible tarea traspasada"
            return response

    def __init__(self, context=None):
        super().__init__(context)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def field_nombreUsuario(self, model):
        return self.ctx.gesttare_field_nombreUsuario(model)

    def field_verConvertirTarea(self, model):
        return self.ctx.gesttare_field_verConvertirTarea(model)

    def field_verTranspasarAnotacion(self, model):
        return self.ctx.gesttare_field_verTranspasarAnotacion(model)

    def field_actIcon(self, model):
        return self.ctx.gesttare_field_actIcon(model)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def queryGrid_notificacionesUsuario(self, model):
        return self.ctx.gesttare_queryGrid_notificacionesUsuario(model)

    def queryGrid_notificacionesUsuarioViejas(self, model):
        return self.ctx.gesttare_queryGrid_notificacionesUsuarioViejas(model)

    def visualizarElemento(self, model, cursor):
        return self.ctx.gesttare_visualizarElemento(model, cursor)

    def borrarActualizacion(self, model, oParam):
        return self.ctx.gesttare_borrarActualizacion(model, oParam)

    def field_color_responsable(self, model):
        return self.ctx.gesttare_field_color_responsable(model)

    def field_color_fondo_icono(self, model):
        return self.ctx.gesttare_field_color_fondo_icono(model)

    def field_titulo_icono(self, model):
        return self.ctx.gesttare_field_titulo_icono(model)

    def convertirTarea(self, model, oParam):
        return self.ctx.gesttare_convertirTarea(model, oParam)

    def transpasarAnotacion(self, model, oParam):
        return self.ctx.gesttare_transpasarAnotacion(model, oParam)

    def aceptarColaborador(self, oParam, cursor):
        return self.ctx.gesttare_aceptarColaborador(oParam, cursor)


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
