# @class_declaration interna #
from YBLEGACY import qsatype
from YBUTILS import gesDoc
# from models.flfactppal.usuarios import usuarios
from models.fllogin.aqn_user import aqn_user as usuarios
from models.flgesttare.gt_timetracking import gt_timetracking as timetracking
import datetime
import time
from models.flgesttare import flgesttare_def
from datetime import date
import hashlib
import json
import calendar

class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
from YBUTILS.APIQSA import APIQSA
from models.flgesttare.gt_controlhorario import gt_controlhorario as controlhorario
import urllib

class gesttare(interna):

    def gesttare_get_model_info(self, model, data, ident, template, where_filter):
        if template == "list":
            return {"groupBoxPadre": "Nº DE TAREAS: {}".format(ident["COUNT"])}
        if template == "master":
            return {"groupBoxPadre": "Nº DE TAREAS: {}".format(ident["PAG"]["COUNT"])}
        if template == "renegociar" or template == "recordatorio" or template == "recordatorioPlanear":
            return {"groupBoxPadre": "Nº DE TAREAS: {}".format(ident["PAG"]["COUNT"])}
        if template == "formRecord":
            nombreUsuario = qsatype.FLUtil.nameUser()
            idcompany = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "idcompany", "idproyecto = '{}'".format(data["idproyecto"])) or None
            id_compania_usuario = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(nombreUsuario)) or None
            
            if idcompany == id_compania_usuario:
                idcliente = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "idcliente", "idproyecto = '{}'".format(data["idproyecto"])) or None

                if idcliente:
                    codcliente = qsatype.FLUtil.sqlSelect(u"gt_clientes", u"nombre", ustr(u"idcliente = '", str(idcliente), u"'"))
                    if codcliente:
                        return {"tareasForm": "Información - Cliente: {}".format(codcliente)}
        return None

    def get_model_info(self, model, data, ident, template, where_filter):
        return self.ctx.gesttare_get_model_info(model, data, ident, template, where_filter)

    def gesttare_fun_totalDays(self, model):
        return 30

    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        if template == "renegociacion":
            return [
                {'verbose_name': 'renegociaProyecto', 'func': 'ren_field_proyecto'},
                {'verbose_name': 'renegociacolorfechavencimiento', 'func': 'ren_color_fecha'},
                {'verbose_name': 'renecogiacolorfechaentrega', 'func': 'ren_color_fechaentrega'}
            ]
        if template == "master":
            fields = [
                {'verbose_name': 'Proyecto', 'func': 'field_proyecto'},
                {'verbose_name': 'Responsable', 'func': 'field_usuario'},
                {'verbose_name': 'Color fecha', 'func': 'color_fecha'},
                {'verbose_name': 'Color nombre', 'func': 'color_nombre'},
                {'verbose_name': 'Color nombre proyecto', 'func': 'color_nombreProyecto'},
                {'verbose_name': 'Color fondo estado', 'func': 'color_fondo_estado'},
                {'verbose_name': 'Color responsable', 'func': 'color_responsable'},
                {'verbose_name': 'Color fechaentrega', 'func': 'color_fechaentrega'},
                {'verbose_name': 'completaIcon', 'func': 'field_completaIcon'},
                {'verbose_name': 'trackingIcon', 'func': 'field_trackingIcon'},
                {'verbose_name': 'completaTitle', 'func': 'field_completaTitle'},
                {'verbose_name': 'adjuntoTarea', 'func': 'fun_totalDays'}       
            ]

        if template == "formRecordcalendarioTareas":
            return [{'verbose_name': 'totalDays', 'func': 'fun_totalDays'}]

        if template == "formRecord" or template == "tareacolaborador":
            return [{'verbose_name': 'adjuntoTarea', 'func': 'field_adjunto'}]

        if template == "recordatorio" or template == "recordatorioPlanear":
            return [
                {'verbose_name': 'renegociaProyecto', 'func': 'ren_field_proyecto_espera'},
                {'verbose_name': 'renegociacolorfechavencimiento', 'func': 'ren_color_fecha_espera'},
                {'verbose_name': 'renecogiacolorfechaentrega', 'func': 'ren_color_fechaentrega_espera'}
            ]

        if template == "revisionTareas":
            return [ {'verbose_name': 'Color fondo estado revision', 'func': 'color_fondo_estado_revision'}]

        if template == "revisionTareasTreinta":
            return [ {'verbose_name': 'Color fondo estado revision', 'func': 'color_fondo_estado_revision'}]

        return fields

    def gesttare_getDesc(self):
        return "nombre"

    def gesttare_field_adjunto(self, model):
        nombre = None
        ficheros = gesDoc.getFiles("gt_tareas", model.pk)
        # idUsuario = qsatype.FLUtil.nameUser()
        # pk = model.pk
        # params = {
        #     'pk': pk,
        #     'prefix': "gt_tareas"
        # }
        # # ficheros = APIQSA.entry_point('post', "gd_documentos", idUsuario, params, 'getFiles') 
        # ficheros = APIQSA.entry_point('post', "gd_documentos", idUsuario, params, 'getFiles')
        adjuntos = []
        if ficheros:
            files = ""
            for file in ficheros:
                adjuntos.append({"id": file, "name": ficheros[file]["nombre"]})
            return adjuntos
            #     files = file + "./."
            # return files
        # if file:
        #     return file["nombre"]
        return nombre

    def gesttare_iniciaValoresLabel(self, model, template, cursor, data):
        if template == "formRecord" or template == "tareacolaborador":
            tiempototal = qsatype.FLUtil.quickSqlSelect("gt_timetracking", "SUM(totaltiempo)", "idtarea = {}".format(cursor.valueBuffer("idtarea"))) or 0
            if not tiempototal:
                return {"tiempoTotal": "Tiempo total: 00:00:00"}
            tiempototal = self.seconds_to_time(tiempototal.total_seconds(), all_in_hours=True)
            return {"tiempoTotal": "Tiempo total: {}".format(tiempototal)}

        return {}

    def gesttare_seconds_to_time(self, seconds, total=False, all_in_hours=False):
        return timetracking.getIface().seconds_to_time(seconds, total, all_in_hours)

    def gesttare_actNuevoComentario(self, model, oParam):
        nombreUsuario = qsatype.FLUtil.nameUser()
        idUsuario = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idusuario", ustr(u"idusuario = '", nombreUsuario, u"'"))
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
        today = qsatype.Date()
        thismonth = today.getMonth()
        formatmonth = today.getMonth() if len(str(today.getMonth())) == 2 else "0" + str(today.getMonth())
        thisyear = today.getYear()
        firstday = qsatype.Date(str(thisyear) + "-" + str(formatmonth) + "-01")

        lastmonthday = calendar.monthrange(thisyear, thismonth)[1]
        lastday = qsatype.Date(str(thisyear) + "-" + str(formatmonth) + "-" + str(lastmonthday))

        fechaDesde = str(firstday - datetime.timedelta(days=7))
        fechaHasta = str(lastday + datetime.timedelta(days=7))
        
        # fromyear = thisyear if thismonth > 1 else thisyear - 1
        # toyear = thisyear if thismonth < 12 else thisyear + 1
        # existe = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"idtarea", ustr(u"extract(month from gt_tareas.fechavencimiento) = ", qsatype.Date().getMonth()))
        # if not existe:
        #     return initFilter
        # initFilter['where'] = u" AND extract(year from gt_tareas.fechavencimiento) = 2020"
        initFilter['where'] = u" AND gt_tareas.fechavencimiento >= '" + fechaDesde[:10] + "' AND gt_tareas.fechavencimiento <= '" + fechaHasta[:10] + "'"
        # initFilter['where'] += u" AND extract(month from gt_tareas.fechavencimiento) = " + str(qsatype.Date().getMonth())
        initFilter['filter'] = {"s_gt_tareas.fechavencimiento__gt": fechaDesde[:10], "s_gt_tareas.fechavencimiento__lt": fechaHasta[:10]}
        return initFilter

    def gesttare_queryGrid_calendarioTareas(self, model):
        proin = "("
        usuario = qsatype.FLUtil.nameUser()
        curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
        curProyectos.select("idusuario = '" + str(usuario) + "'")
        while curProyectos.next():
            curProyectos.setModeAccess(curProyectos.Browse)
            curProyectos.refreshBuffer()
            # proin.append(curProyectos.valueBuffer("idproyecto"))
            proin = proin + "'" + str(curProyectos.valueBuffer("idproyecto")) + "', "
        proin = proin + " null)"
        query = {}
        query["tablesList"] = ("gt_tareas, aqn_user, gt_proyectos")
        query["select"] = ("gt_tareas.idtarea, aqn_user.email, aqn_user.usuario, gt_tareas.idproyecto, gt_tareas.codestado, gt_proyectos.nombre ,gt_tareas.codespacio, gt_tareas.idusuario, gt_tareas.fechavencimiento, gt_tareas.nombre, extract(day from gt_tareas.fechavencimiento) as day, extract(month from gt_tareas.fechavencimiento) as month, extract(year from gt_tareas.fechavencimiento) as year, extract(dow from date_trunc('month', gt_tareas.fechavencimiento)) as firstDay")
        # query["select"] = ("gt_tareas.idtarea, gt_tareas.fechainicio, gt_tareas.descripcion")
        query["from"] = ("gt_tareas INNER JOIN aqn_user ON gt_tareas.idusuario = aqn_user.idusuario INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto")
        query["where"] = ("gt_tareas.fechavencimiento is not null AND  gt_proyectos.archivado = false AND gt_tareas.idproyecto IN " + proin + " AND not gt_tareas.resuelta AND 1=1")
        query["limit"] = 100
        # query["groupby"] = " articulos.referencia, articulos.descripcion"
        # query["orderby"] = "MAX(pedidoscli.fecha) DESC"
        return query

    def gesttare_getListaTarea(self, model, oParam):
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
        if nuevaFecha:
            cursor.setValueBuffer("fechavencimiento", nuevaFecha)
            if not cursor.commitBuffer():
                return False
        return True

    def gesttare_ren_field_proyecto(self, model):
        proyecto = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "nombre", "idproyecto = '{}'".format(str(model["gt_tareas.idproyecto"]))) or ""
        idcliente = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "idcliente", "idproyecto = '{}'".format(str(model["gt_tareas.idproyecto"]))) or None
        if idcliente:
            codcliente = qsatype.FLUtil.sqlSelect(u"gt_clientes", u"codcliente", ustr(u"idcliente = '", str(idcliente), u"'"))
            if codcliente:
                proyecto = "#" + codcliente + " " + proyecto
        return proyecto

    def gesttare_ren_field_proyecto_espera(self, model):
        proyecto = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "nombre", "idproyecto = '{}'".format(str(model.idproyecto.idproyecto))) or ""
        idcliente = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "idcliente", "idproyecto = '{}'".format(str(model.idproyecto.idproyecto))) or None
        if idcliente:
            codcliente = qsatype.FLUtil.sqlSelect(u"gt_clientes", u"codcliente", ustr(u"idcliente = '", str(idcliente), u"'"))
            if codcliente:
                proyecto = "#" + codcliente + " " + proyecto
        return proyecto

    def gesttare_field_proyecto(self, model):
        # proyecto = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "nombre", "idproyecto = '{}'".format(model.idproyecto)) or ""
        nombreUsuario = qsatype.FLUtil.nameUser()
        # idcompany = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "idcompany", "idproyecto = '{}'".format(data["idproyecto"])) or None
        id_compania_usuario = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(nombreUsuario))
        proyecto = ""
        
        try:
            proyecto = model.idproyecto.nombre
            # idcliente = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "idcliente", "idproyecto = '{}'".format(model.idproyecto)) or None
            idcliente = model.idproyecto.idcliente
            if idcliente:
                # codcliente = qsatype.FLUtil.sqlSelect(u"gt_clientes", u"codcliente", ustr(u"idcliente = '", str(idcliente), u"'"))
                codcliente = model.idproyecto.idcliente.codcliente
                if codcliente and model.idproyecto.idcompany.idcompany == id_compania_usuario:
                    proyecto = "#" + codcliente + " " + proyecto
        except:
            pass
        return proyecto

    def gesttare_field_completaIcon(self, model):
        if model.resuelta:
            return "check_box"
        else:
            return "check_box_outline_blank"

        return ""

    def gesttare_field_trackingIcon(self, model):
        username = qsatype.FLUtil.nameUser()
        tareaactiva = qsatype.FLUtil.quickSqlSelect("aqn_user", "idtareaactiva", "idusuario = '{}'".format(username))
        
        if model.idtarea == tareaactiva:
            return "pause"
        else:
            return "play_arrow"

        return ""

    def gesttare_field_completaTitle(self, model):
        if model.resuelta:
            return "Abrir tarea"
        else:
            return "Completar tarea"

        return ""

    def gesttare_field_usuario(self, model):
        nombre_usuario = ""
        try:
            if not model.idusuario:
                return nombre_usuario
            nombre_usuario = "@" + model.idusuario.usuario
        except Exception:
            pass
        return nombre_usuario

    def gesttare_color_nombre(self, model):
        username = qsatype.FLUtil.nameUser()
        tareaactiva = qsatype.FLUtil.quickSqlSelect("aqn_user", "idtareaactiva", "idusuario = '{}'".format(username))
        
        if model.idtarea and tareaactiva and model.idtarea == tareaactiva:
            return "fcSuccessMango"
        elif model.fechaentrega and str(model.fechaentrega) < qsatype.Date().toString()[:10] or model.fechavencimiento and str(model.fechavencimiento) < qsatype.Date().toString()[:10]:
            return "fcDanger"

        return ""

    def gesttare_color_nombreProyecto(self, model):
        username = qsatype.FLUtil.nameUser()
        tareaactiva = qsatype.FLUtil.quickSqlSelect("aqn_user", "idtareaactiva", "idusuario = '{}'".format(username))
        id_compania_usuario = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(username))
        tipo_participante = qsatype.FLUtil.quickSqlSelect("gt_particproyecto", "tipo", "idusuario = '{}' AND idproyecto = {}".format(username, str(model.idproyecto.idproyecto)))
        color = ""
        if tipo_participante == "observador":
            color += "OBSER "
        if model.idproyecto.idcompany.idcompany != id_compania_usuario and tipo_participante != "observador":
            color += "COL "
        if model.idproyecto.idcompany.idcompany == id_compania_usuario:
            color += "INTERNO_EMPRESA "
        if model.fechaentrega and str(model.fechaentrega) < qsatype.Date().toString()[:10] or model.fechavencimiento and str(model.fechavencimiento) < qsatype.Date().toString()[:10]:
            color += "fcDanger"

        return color

    def gesttare_color_fondo_estado(self, model):
        if model.codestado:
            if model.codestado.codestado == "Por Hacer":
                return "naranja"
            elif model.codestado.codestado == "Recurrente":
                return "lila"
            elif model.codestado.codestado == "Hecho":
                return "verde"
            elif model.codestado.codestado == "En espera":
                return "amarillo"
        return ""

    def gesttare_color_fondo_estado_revision(self, model):
        if model["gt_tareas.codestado"]:
            if model["gt_tareas.codestado"] == "Por Hacer":
                return "naranja"
            elif model["gt_tareas.codestado"] == "Recurrente":
                return "lila"
            elif model["gt_tareas.codestado"] == "Hecho":
                return "verde"
            elif model["gt_tareas.codestado"] == "En espera":
                return "amarillo"
        return ""

    def gesttare_color_responsable(self, model):
        if hasattr(model.idusuario, 'idusuario'):
            return "responsable"

        return ""

    def gesttare_color_fecha(self, model):
        if model.fechavencimiento and str(model.fechavencimiento) < qsatype.Date().toString()[:10]:
            return "fcDanger"
        if model.fechavencimiento and model.fechaentrega and model.fechaentrega < model.fechavencimiento:
            return "fcWarning"
        return ""

    def gesttare_color_fechaentrega(self, model):
        if model.fechaentrega and str(model.fechaentrega) < qsatype.Date().toString()[:10]:
            return "fcDanger"
        if model.fechavencimiento and model.fechaentrega and model.fechaentrega < model.fechavencimiento:
            return "fcWarning"
        return ""

    def gesttare_ren_color_fecha(self, model):
        if model["gt_tareas.fechavencimiento"] and str(model["gt_tareas.fechavencimiento"]) < qsatype.Date().toString()[:10]:
            return "fcDanger"
        if model["gt_tareas.fechavencimiento"] and model["gt_tareas.fechaentrega"] and model["gt_tareas.fechaentrega"] < model["gt_tareas.fechavencimiento"]:
            return "fcWarning"
        return ""

    def gesttare_ren_color_fechaentrega(self, model):
        if model["gt_tareas.fechaentrega"] and str(model["gt_tareas.fechaentrega"]) < qsatype.Date().toString()[:10]:
            return "fcDanger"
        if model["gt_tareas.fechavencimiento"] and model["gt_tareas.fechaentrega"] and model["gt_tareas.fechaentrega"] < model["gt_tareas.fechavencimiento"]:
            return "fcWarning"
        return ""

    def gesttare_ren_color_fecha_espera(self, model):
        if model.fechavencimiento and str(model.fechavencimiento) < qsatype.Date().toString()[:10]:
            return "fcDanger"
        if model.fechavencimiento and model.fechaentrega and model.fechaentrega <  model.fechavencimiento:
            return "fcWarning"
        return ""

    def gesttare_ren_color_fechaentrega_espera(self, model):
        if model.fechaentrega and str(model.fechaentrega) < qsatype.Date().toString()[:10]:
            return "fcDanger"
        if model.fechavencimiento and model.fechaentrega and model.fechaentrega < model.fechavencimiento:
            return "fcWarning"
        return ""

    def gesttare_uploadFile(self, model, oParam):
        idUsuario = qsatype.FLUtil.nameUser()
        comentario = ""
        if "comentario" in oParam:
            comentario = oParam['comentario']

        if len(oParam["FILES"]) > 0 or "comentario" in oParam:
            if "comentario_publico" in oParam:
                params = {
                    "comentario": oParam['comentario'],
                    "idtarea": model.idtarea
                }
                pk = APIQSA.entry_point('post', "gt_comentarios", idUsuario, params, "comentario_publico_observador")
                pk = pk.decode("utf-8")
                if not gesDoc.fileUpload("gt_comentarios", pk, oParam['FILES']):
                    return False
                return True
            cursor = qsatype.FLSqlCursor(u"gt_comentarios")
            cursor.setModeAccess(cursor.Insert)
            cursor.refreshBuffer()
            cursor.setValueBuffer(u"idtarea", model.idtarea)
            cursor.setValueBuffer(u"fecha", str(qsatype.Date())[:10])
            cursor.setValueBuffer(u"hora", str(qsatype.Date())[-8:])
            cursor.setValueBuffer(u"comentario", comentario)
            cursor.setValueBuffer(u"hdedicadas", 0)
            cursor.setValueBuffer(u"costehora", 0)
            cursor.setValueBuffer(u"coste", 0)
            cursor.setValueBuffer(u"idusuario", idUsuario)
            if "comentario_publico" in oParam:
                cursor.setValueBuffer(u"publico", True)
            else:
                cursor.setValueBuffer(u"publico", False)
            if not cursor.commitBuffer():
                print("algo salio mal")
                return False
            if not gesDoc.fileUpload("gt_comentarios", cursor.valueBuffer("idcomentario"), oParam['FILES']):
                return False

            return True

        resul = {}
        resul["return_data"] = False
        resul["msg"] = "Escribe un comentario o adjunta un archivo"

        return resul

    def gesttare_uploadFileTarea(self, model, oParam):
        # if not gesDoc.fileUpload("gt_tareas", model.idtarea, oParam['FILES']):
        #     return False
        if len(oParam["FILES"]) > 0:
            return True

        resul = {}
        resul["return_data"] = False
        resul["msg"] = "No hay seleccionado archivo para adjuntar"

        return resul

    def gesttare_login(self, oParam):
        data = []
        username = oParam["user"]
        password = oParam["pass"]
        usuario = usuarios.objects.filter(idusuario__exact=username)
        if len(usuario) == 0:
            data.append({"result": False})
            data.append({"error": "No existe el usuario"})
            return data
        usuario = usuarios.objects.get(idusuario=username)
        md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
        if usuario.password != md5passwd:
            data.append({"result": False})
            data.append({"error": "Error en autenticación"})
            return data
        data.append({"result": True})
        return data

    def gesttare_getpryus(self, appid, email):
        _i = self.iface
        idusuario = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idusuario", u"email = '" + str(email) + u"'")
        response = {}
        if not idusuario:
            response["result"] = False
            response["error"] = "No existe el usuario de dailyjob, por tanto no tienes permisos para crear tareas en el proyecto"
            response["nombreProyecto"] = " "
            response["username"] = email
            return response
        if appid == "23553220-e1b3-4592-a5de-fb41a08c60c8":
            proyectos = _i.dameProyectos(idusuario)
            usuarios = _i.dameUsuarios(idusuario)
            response["projects"] = proyectos
            response["users"] = usuarios
        else:
            response["result"] = False
            response["error"] = "Error en autenticación"

        return response

    def gesttare_damepryus(self, appid, email):
        _i = self.iface
        idusuario = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idusuario", u"email = '" + str(email) + u"'")
        data = []
        if not idusuario:
            data.append({"result": False})
            data.append({"error": "No existe el usuario de dailyjob, por tanto no tienes permisos para crear tareas en el proyecto"})
            return data
        if appid == "23553220-e1b3-4592-a5de-fb41a08c60c8":
            proyectos = _i.dameProyectos(idusuario)
            usuarios = _i.dameUsuarios(idusuario)
            data.append({"projects": proyectos})
            data.append({"users": usuarios})
        else:
            data.append({"result": False})
            data.append({"error": "Error en autenticación"})

        return data

    def gesttare_dameProyectos(self, idusuario):
        _i = self.iface
        proyectos = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_proyectos, gt_particproyecto")
        q.setSelect("gt_proyectos.idproyecto, gt_proyectos.nombre")
        q.setFrom("gt_proyectos INNER JOIN gt_particproyecto ON gt_proyectos.idproyecto = gt_particproyecto.idproyecto")
        q.setWhere(u"idusuario = '" + str(idusuario) + "'")

        if not q.exec_():
            print("Error inesperado")
            return []

        while q.next():
            participantes =  []
            qParticPro = qsatype.FLSqlQuery()
            qParticPro.setTablesList(u"gt_particproyecto")
            qParticPro.setSelect("gt_particproyecto.idusuario")
            qParticPro.setFrom("gt_particproyecto")
            qParticPro.setWhere(u"idproyecto = '" + str(q.value(0)) + "'")

            if not qParticPro.exec_():
                print("Error inesperado")
                return []

            while qParticPro.next():
                participantes.append(qParticPro.value(0))
            hitos = _i.dameHitos(q.value(0))
            if hitos:
                proyectos.append({"codigo": str(q.value(0)), "descripcion": str(q.value(1)), "hitos": hitos, "participantes": participantes})

        return proyectos

    def gesttare_dameHitos(self, idproyecto):
        hitos = []
        qHitos = qsatype.FLSqlQuery()
        qHitos.setTablesList(u"gt_hitosproyecto")
        qHitos.setSelect("idhito, nombre")
        qHitos.setFrom("gt_hitosproyecto")
        qHitos.setWhere(u"idproyecto = '" + str(idproyecto) + "'")

        if not qHitos.exec_():
            print("No tengo hitos")
            return []

        while qHitos.next():
            hitos.append({"idhito": str(qHitos.value(0)), "nombre": str(qHitos.value(1))})
        return hitos

    def gesttare_dameUsuarios(self, idusuario):
        usuarios = []
        idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", u"idusuario = '" + str(idusuario) + u"'")
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"aqn_user")
        q.setSelect("idusuario, email, nombre, apellidos")
        q.setFrom("aqn_user")
        q.setWhere(u"idcompany = '" + str(idcompany) + "'")

        if not q.exec_():
            print("Error inesperado")
            return []
        while q.next():
            nombre = str(q.value(2) or "") + " " + str(q.value(3) or "")
            usuarios.append({"codigo": str(q.value(0)), "email": str(q.value(1)), "nombre": str(nombre)})

        return usuarios

    def gesttare_calcula_totaltiempo(self, cursor):
        formato = "%H:%M:%S"
        horainicio = str(cursor.valueBuffer("horainicio"))
        if len(horainicio) == 5:
            horainicio += ":00"
        horafin = str(cursor.valueBuffer("horafin"))
        if len(horafin) == 5:
            horafin += ":00"
        hfin = datetime.datetime.strptime(horafin, formato)
        hinicio = datetime.datetime.strptime(horainicio, formato)
        totaltiempo = hfin - hinicio
        totaltiempo = str(totaltiempo)
        if len(totaltiempo) < 8:
            totaltiempo = "0" + totaltiempo
        if len(totaltiempo) > 8:
            totaltiempo = totaltiempo[8:]
        return totaltiempo

    def gesttare_startstop(self, model, oParam, cursor):
        now = qsatype.Date()
        user_name = qsatype.FLUtil.nameUser()
        msg = ""
        response = {}
        # id_compania = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(user_name))
        # id_plan = qsatype.FLUtil.quickSqlSelect("aqn_companies", "idplan", "idcompany = '{}'".format(id_compania))
        
        # if id_plan == 1:
        #     response = {}
        #     response["resul"] = True
        #     response["msg"] = "Debes tener un plan de pago para esta funcionalidad"
        #     return response
        tengopermiso = flgesttare_def.iface.compruebaPermisosPlan("startstop")
        # response = self.plan_compania(user_name)
        if tengopermiso != True:
            return tengopermiso

        tipo_participante = tipo_participante = qsatype.FLUtil.quickSqlSelect("gt_particproyecto", "tipo", "idusuario = '{}' AND idproyecto = {}".format(user_name, str(cursor.valueBuffer("idproyecto"))))

        if tipo_participante == "observador":
            response["resul"] = True
            response["msg"] = "No puedes añadir tiempo a los proyectos en los que tienes un rol de observación"
            return response

        tramoactivo = qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idusuario = {} AND horafin IS NULL".format(user_name))
        if not tramoactivo:
            start = controlhorario.getIface().start({}, oParam)
            if "resul" in start and start["resul"] != True:
                return start

        # Comprobamos que si hay que renegociar, ademas iniciamos el control de tiempo
        if not oParam or "confirmacion" not in oParam:
            # renegociar = qsatype.FLUtil.quickSqlSelect("gt_tareas", "COUNT(idtarea)", "resuelta = false AND fechavencimiento < '{}' AND idusuario = '{}'".format(str(qsatype.Date())[:10] ,user_name)) or 0
            q = qsatype.FLSqlQuery()
            q.setTablesList(u"gt_proyectos, gt_tareas")
            q.setSelect(u"t.idtarea")
            q.setFrom(u"gt_tareas t INNER JOIN gt_proyectos p ON t.idproyecto=p.idproyecto")
            q.setWhere(u"t.resuelta = false AND t.fechavencimiento < '{}' AND t.idusuario = '{}' AND p.archivado = false".format(str(qsatype.Date())[:10] ,user_name))
            if not q.exec_():
                return []
            renegociar = q.size() or 0
            if renegociar > 0:
                response["status"] = 2
                response["confirm"] = "Antes de continuar con nuevas tareas deberías revisar las tareas que tienes atrasadas. </br></br> ¿Quieres renegociar ahora?"
                response["serverAction"] = "startstop"
                response["customButtons"] = [{"accion": "goto","nombre": "Sí", "url": "/gesttare/gt_tareas/custom/renegociar"}, {"accion": "cancel","nombre": "No"}]
                # response["goto"] = {"nombre": "Sí", "url": "/gesttare/gt_tareas/custom/renegociar"}
                return response

        cur_track = qsatype.FLSqlCursor("gt_timetracking")
        cur_track.select("idusuario = '{}' AND horafin IS NULL".format(user_name))

        if cur_track.first():
            cur_track.setModeAccess(cur_track.Edit)
            cur_track.refreshBuffer()

            cur_track.setValueBuffer("horafin", now.toString()[-8:])
            cur_track.setValueBuffer("totaltiempo", self.calcula_totaltiempo(cur_track))
            cur_track.setValueBuffer(u"coste", flgesttare_def.iface.calcula_costetiempo("timetracking", cur_track))

            if not cur_track.commitBuffer():
                print("Ocurrió un error al actualizar el registro de gt_timetracking")
                return False

        cur_user = qsatype.FLSqlCursor("aqn_user")
        cur_user.select("idusuario = '{}'".format(user_name))
        if not cur_user.first():
            print("No se encontró el usuario")
            return False

        cur_user.setModeAccess(cur_user.Edit)
        cur_user.refreshBuffer()

        if cur_track.valueBuffer("idtarea") == cursor.valueBuffer("idtarea"):
            msg += "Time tracking detenido"
            cur_user.setNull("idtareaactiva")
        else:
            msg += "Time tracking iniciado"
            cur_track.setModeAccess(cur_track.Insert)
            cur_track.refreshBuffer()

            cur_track.setValueBuffer("fecha", now.toString()[:10])
            cur_track.setValueBuffer("horainicio", now.toString()[-8:])
            cur_track.setValueBuffer("idusuario", user_name)
            cur_track.setValueBuffer("idtarea", cursor.valueBuffer("idtarea"))

            if not cur_track.commitBuffer():
                print("Ocurrió un error al guardar el registro de gt_timetracking")
                return False

            cur_user.setValueBuffer("idtareaactiva", cursor.valueBuffer("idtarea"))

        if not cur_user.commitBuffer():
            print("Ocurrió un error al actualizar la tarea activa del usuario")
            return False
        response = {}
        response["resul"] = True
        response["msg"] = msg
        return response

    def gesttare_completar_tarea(self, model, cursor):
        response = {}
        usuario = qsatype.FLUtil.nameUser()
        id_proyecto = qsatype.FLUtil.sqlSelect("gt_tareas", "idproyecto", "idtarea = {}".format(str(cursor.valueBuffer("idtarea"))))
        tipo_participante = qsatype.FLUtil.sqlSelect("gt_particproyecto", "tipo", "idproyecto = {} AND idusuario = {}".format(str(id_proyecto), str(usuario)))
        response = {}
        if tipo_participante == "observador":
            response['status'] = 1
            response["msg"] = "No puedes completar la tarea con el rol de observación"
            return response
        resuelta = cursor.valueBuffer("resuelta")
        cursor.setValueBuffer("resuelta", not resuelta)

        if not cursor.commitBuffer():
            print("Ocurrió un error al actualizar la tarea")
            return False
        # qsatype.APIQSA.entry_point("POST", "gt_tareas", qsatype.FLUtil.nameUser(), {"pk": model.pk, "data": {"resuelta": not resuelta}}, "update")
        response["resul"] = True
        if resuelta:
            response["msg"] = "Tarea abierta"
        else:
            response["msg"] = "Tarea completada"
        return response

    def gesttare_abrir_tarea(self, model, cursor):
        response = {}
        resuelta = cursor.valueBuffer("resuelta")
        cursor.setValueBuffer("resuelta", not resuelta)

        if not cursor.commitBuffer():
            print("Ocurrió un error al actualizar la tarea")
            return False

        response["resul"] = True
        if resuelta:
            response["msg"] = "Tarea abierta"
        return response

    def gesttare_un_dia(self, model, cursor):
        response = {}
        # fecha = cursor.valueBuffer("fechavencimiento")
        # if fecha:
        fecha = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').date()

        increDia = fecha.today() + datetime.timedelta(days=1)

        cursor.setValueBuffer("fechavencimiento", increDia)

        if not cursor.commitBuffer():
            print("Ocurrió un error al actualizar la tarea")
            return False

        response["resul"] = True
        response["msg"] = "Tarea planeada para el día siguiente"

        # else:
        #     response["resul"] = True
        #     response["msg"] = "No hay fecha de ejecución"
        # if fecha:
        #     response["msg"] = "Tarea planificada para mañana"
        # else:
        #     response["msg"] = "No hay fecha de ejecución"
        return response

    def gesttare_semana_siguiente(self, model, cursor):
        response = {}
        # fecha = cursor.valueBuffer("fechavencimiento")
        # if fecha:
        fecha = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').date()

        increDia = fecha + datetime.timedelta(days=(7 - fecha.weekday()))

        cursor.setValueBuffer("fechavencimiento", increDia)

        if not cursor.commitBuffer():
            print("Ocurrió un error al actualizar la tarea")
            return False

        response["resul"] = True
        response["msg"] = "Tarea planeada para el Lunes siguiente"

        # else:
        #     response["resul"] = True
        #     response["msg"] = "No hay fecha de ejecución"
        # if fecha:
        #     response["msg"] = "Tarea planificada para mañana"
        # else:
        #     response["msg"] = "No hay fecha de ejecución"
        return response

    def gesttare_elegir_fecha(self, model, cursor):
        response = {}
        response['status'] = -1
        response['data'] = {}
        response["prefix"] = "gt_tareas"
        response["title"] = "Elegir fecha"
        # response["confirm"] = "</br></br> ¿Quieres continuar?"
        response["serverAction"] = "elegir_fecha"
        response["customButtons"] = [{"accion": "serverAction", "pk": cursor.valueBuffer("idtarea"), "nombre": "Programar fecha", "serverAction": "fecha_elegida", "className": "creaAnotacionButton"}]
        
        response['params'] = [
            {
                "tipo": 26,
                "verbose_name": "Fecha",
                "key": "fecha",
                "validaciones": None
            }
        ]
        
        return response

    def gesttare_fecha_elegida(self, model, oParam, cursor):
        response = {}
        # fecha = cursor.valueBuffer("fechavencimiento")
        fecha_terminado_hito = qsatype.FLUtil().quickSqlSelect("gt_hitosproyecto", "fechaterminado", "idhito = {}".format(cursor.valueBuffer("idhito")))
        hoy = datetime.date.today()
        if oParam["fecha"]:
            if fecha_terminado_hito:
                if str(fecha_terminado_hito) >= oParam["fecha"]:
                    if str(hoy) <= oParam["fecha"]:
                        if cursor.valueBuffer("fechaentrega"):
                            if cursor.valueBuffer("fechaentrega") >= oParam["fecha"]:
                                increDia = oParam["fecha"]

                                cursor.setValueBuffer("fechavencimiento", increDia)

                                if not cursor.commitBuffer():
                                    print("Ocurrió un error al actualizar la tarea")
                                    return False

                                response["resul"] = True
                                response["msg"] = "Tarea planeada para la fecha elegida"
                            else:
                                response["status"] = 1
                                response["msg"] = "La fecha de ejecución no puede ser superior a la fecha de entrega"
                        else:
                            increDia = oParam["fecha"]

                            cursor.setValueBuffer("fechavencimiento", increDia)

                            if not cursor.commitBuffer():
                                print("Ocurrió un error al actualizar la tarea")
                                return False

                            response["resul"] = True
                            response["msg"] = "Tarea planeada para la fecha elegida"
                    else:
                        response["status"] = 1
                        response["msg"] = "La fecha de ejecución no puede ser antarior al día de hoy"

                else:
                    response["status"] = 1
                    response["msg"] = "La fecha de finalización del hito es {}. Selecciona una fecha anterior o igual a esa fecha, o modifica la fecha de finalización del hito pulsando <a href='https://app.dailyjob.io/gesttare/gt_hitosproyecto/{}' target='_blank'>aquí</a>".format(str(datetime.datetime.strptime(str(fecha_terminado_hito), '%Y-%m-%d').strftime("%d/%m/%y")), cursor.valueBuffer("idhito"))
            else:
                if str(hoy) <= oParam["fecha"]:
                    if cursor.valueBuffer("fechaentrega"):
                        if cursor.valueBuffer("fechaentrega") >= oParam["fecha"]:
                            increDia = oParam["fecha"]

                            cursor.setValueBuffer("fechavencimiento", increDia)

                            if not cursor.commitBuffer():
                                print("Ocurrió un error al actualizar la tarea")
                                return False

                            response["resul"] = True
                            response["msg"] = "Tarea planeada para la fecha elegida"
                        else:
                            response["status"] = 1
                            response["msg"] = "La fecha de ejecución no puede ser superior a la fecha de entrega"
                    else:
                        increDia = oParam["fecha"]

                        cursor.setValueBuffer("fechavencimiento", increDia)

                        if not cursor.commitBuffer():
                            print("Ocurrió un error al actualizar la tarea")
                            return False

                        response["resul"] = True
                        response["msg"] = "Tarea planeada para la fecha elegida"
                else:
                    response["status"] = 1
                    response["msg"] = "La fecha de ejecución no puede ser antarior al día de hoy"
        else:
            response["status"] = 1
            response["msg"] = "Hay que indicar una fecha"
        return response

    def gesttare_quitar_fecha_modal(self, model, cursor):
        response = {}
        response['status'] = -1
        response['data'] = {}
        response["prefix"] = "gt_tareas"
        response["title"] = "Selecciona el estado de la tarea"
        # response["confirm"] = "</br></br> ¿Quieres continuar?"
        response["serverAction"] = "quitar_fecha"
        response["customButtons"] = [{"accion": "serverAction", "pk": cursor.valueBuffer("idtarea"), "nombre": "En espera", "serverAction": "quitar_fecha_espera", "className": "creaAnotacionButton"}, {"accion": "serverAction", "pk": cursor.valueBuffer("idtarea"), "nombre": "Por Hacer", "serverAction": "quitar_fecha_hacer", "className": "creaAnotacionButton"}]
        
        response['params'] = [
        ]
        
        return response

    def gesttare_quitar_fecha_espera(self, model, cursor):
        response = {}
        fecha = cursor.valueBuffer("fechavencimiento")
        if fecha:

            cursor.setValueBuffer("fechavencimiento", None)
            cursor.setValueBuffer("codestado", "En espera")

            if not cursor.commitBuffer():
                print("Ocurrió un error al actualizar la tarea")
                return False

            response["resul"] = True
            response["msg"] = "Fecha de ejecución eliminada y tarea en espera"

        else:
            response["resul"] = True
            response["msg"] = "No hay fecha de ejecución"
        # if fecha:
        #     response["msg"] = "Tarea planificada para mañana"
        # else:
        #     response["msg"] = "No hay fecha de ejecución"
        return response

    def gesttare_quitar_fecha_hacer(self, model, cursor):
        response = {}
        fecha = cursor.valueBuffer("fechavencimiento")
        if fecha:

            cursor.setValueBuffer("fechavencimiento", None)
            cursor.setValueBuffer("codestado", "Por Hacer")

            if not cursor.commitBuffer():
                print("Ocurrió un error al actualizar la tarea")
                return False

            response["resul"] = True
            response["msg"] = "Fecha de ejecución eliminada y tarea en por hacer"

        else:
            response["resul"] = True
            response["msg"] = "No hay fecha de ejecución"
        # if fecha:
        #     response["msg"] = "Tarea planificada para mañana"
        # else:
        #     response["msg"] = "No hay fecha de ejecución"
        return response


    def gesttare_ejecucion_hoy(self, model, cursor):
        response = {}
        fecha = cursor.valueBuffer("fechavencimiento")
        if fecha:
            fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()

            increDia = fecha.today()

            cursor.setValueBuffer("fechavencimiento", increDia)

            if not cursor.commitBuffer():
                print("Ocurrió un error al actualizar la tarea")
                return False

            response["resul"] = True
            response["msg"] = "Tarea planeada para hoy"

        else:
            increDia = date.today() 

            cursor.setValueBuffer("fechavencimiento", increDia)

            if not cursor.commitBuffer():
                print("Ocurrió un error al actualizar la tarea")
                return False

            response["resul"] = True
            response["msg"] = "Tarea planeada para hoy"
        # if fecha:
        #     response["msg"] = "Tarea planificada para mañana"
        # else:
        #     response["msg"] = "No hay fecha de ejecución"
        return response


    def gesttare_incrementar_dia(self, model, cursor):
        usuario = qsatype.FLUtil.nameUser()
        id_proyecto = qsatype.FLUtil.sqlSelect("gt_tareas", "idproyecto", "idtarea = {}".format(str(cursor.valueBuffer("idtarea"))))
        tipo_participante = qsatype.FLUtil.sqlSelect("gt_particproyecto", "tipo", "idproyecto = {} AND idusuario = {}".format(str(id_proyecto), str(usuario)))
        response = {}
        if tipo_participante == "observador":
            response['status'] = 1
            response["msg"] = "No puedes modificar la fecha de ejecución con el rol de observación"
            return response
        response['status'] = -1
        response['data'] = {}
        response["prefix"] = "gt_tareas"
        response["title"] = "Posponer tarea"
        # response["confirm"] = "</br></br> ¿Quieres continuar?"
        response["serverAction"] = "incrementar dia"
        response["customButtons"] = [{"accion": "serverAction", "pk": cursor.valueBuffer("idtarea"), "nombre": "Hoy", "serverAction": "ejecucion_hoy", "className": "creaAnotacionButton"}, {"accion": "serverAction", "pk": cursor.valueBuffer("idtarea"), "nombre": "Mañana", "serverAction": "un_dia", "className": "creaAnotacionButton"}, {"accion": "serverAction", "pk": cursor.valueBuffer("idtarea"), "nombre": "Próximo lunes", "serverAction": "semana_siguiente", "className": "creaAnotacionButton"}, {"accion": "serverAction", "pk": cursor.valueBuffer("idtarea"), "nombre": "Elegir fecha", "serverAction": "elegir_fecha", "className": "creaAnotacionButton"}, {"accion": "serverAction", "pk": cursor.valueBuffer("idtarea"), "nombre": "quitar fecha", "serverAction": "quitar_fecha_modal", "className": "creaAnotacionButton"}]
        
        response['params'] = [
            
        ]
        
        return response

    def gesttare_creartarea(self, oParam):
        data = []
        if "project" not in oParam or not oParam["project"]:
            data.append({"result": False})
            data.append({"error": "No perteneces al proyecto consulta reponsable"})
            return data
        # usuario = usuarios.objects.filter(idusuario__exact=oParam["person"])
        usuario = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idusuario", ustr(u"idusuario = '", oParam["person"], u"'"))
        if not usuario:
            data.append({"result": False})
            data.append({"error": "No existe el usuario"})
            return data
        existe = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"idproyecto", ustr(u"idproyecto = '", oParam["project"], "'"))
        if not existe:
            data.append({"result": False})
            data.append({"error": "No existe el proyecto"})
            return data
        pertenece = qsatype.FLUtil.sqlSelect(u"gt_particproyecto", u"idproyecto", ustr(u"idusuario = '", str(oParam["person"]), u"' AND idproyecto = '", oParam["project"], "'"))
        if not pertenece:
            data.append({"result": False})
            data.append({"error": "No perteneces al proyecto consulta reponsable"})
            return data
        if oParam["appid"] == "23553220-e1b3-4592-a5de-fb41a08c60c8":
            idhito = None
            q = qsatype.FLSqlQuery()
            q.setTablesList(u"gt_hitosproyecto")
            q.setSelect(u"idhito")
            q.setFrom(u"gt_hitosproyecto")
            q.setWhere(u"idproyecto = '" + str(oParam["project"].upper()) + "'")

            if not q.exec_():
                return []
            if q.size() > 100:
                return []

            if q.next():
                idhito = q.value("idhito")

            curTarea = qsatype.FLSqlCursor(u"gt_tareas")
            curTarea.setModeAccess(curTarea.Insert)
            curTarea.refreshBuffer()
            curTarea.setActivatedBufferCommited(True)
            curTarea.setValueBuffer(u"idproyecto", oParam["project"].upper())
            curTarea.setValueBuffer(u"codestado", oParam["state"])
            curTarea.setValueBuffer(u"nombre", oParam["name"])
            curTarea.setValueBuffer(u"idusuario", oParam["person"])
            curTarea.setValueBuffer(u"descripcion", oParam["description"])
            curTarea.setValueBuffer(u"resuelta", False)
            curTarea.setValueBuffer(u"idhito", idhito)
            if oParam["date"] and oParam["date"] != u"undefined":
                curTarea.setValueBuffer(u"fechavencimiento", oParam["date"])

            if not curTarea.commitBuffer():
                data.append({"result": False})
                data.append({"error": "Error en commit"})
            else:
                data.append({"result": True})
                data.append({"ok": "Tarea creada"})
        else:
            data.append({"result": False})
            data.append({"error": "Error en autenticación"})
        return data

    def gesttare_createtask(self, oParam):
        response = {}
        if "project" not in oParam or not oParam["project"]:
            nombreProyecto = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"nombre", ustr(u"idproyecto = '", str(oParam["project"]), u"'"))
            response["result"] = False
            response["error"] = "No tienes permisos para crear tareas en el proyecto"
            response["nombreProyecto"] = nombreProyecto
            response["username"] = oParam["person"]
            return response
        # usuario = usuarios.objects.filter(idusuario__exact=oParam["person"])
        usuario = qsatype.FLUtil.sqlSelect(u"aqn_user", u"usuario", ustr(u"idusuario = '", oParam["person"], u"'"))
        if not usuario:
            response["result"] = False
            response["error"] = "No existe el usuario de dailyjob, por tanto no tienes permisos para crear tareas en el proyecto"
            response["nombreProyecto"] = " "
            response["username"] = oParam["person"]
        pertenece = qsatype.FLUtil.sqlSelect(u"gt_particproyecto", u"idproyecto", ustr(u"idusuario = '", str(oParam["person"]), u"' AND idproyecto = '", oParam["project"], "'"))
        if not pertenece:
            nombreProyecto = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"nombre", ustr(u"idproyecto = '", oParam["project"], u"'"))
            response["result"] = False
            response["error"] = "No tienes permisos para crear tareas en el proyecto"
            response["nombreProyecto"] = nombreProyecto
            response["username"] = usuario
            return response
        if oParam["appid"] == "23553220-e1b3-4592-a5de-fb41a08c60c8":
            # idhito = None
            # q = qsatype.FLSqlQuery()
            # q.setTablesList(u"gt_hitosproyecto")
            # q.setSelect(u"idhito")
            # q.setFrom(u"gt_hitosproyecto")
            # q.setWhere(u"idproyecto = '" + str(oParam["project"].upper()) + "'")

            # if not q.exec_():
            #     return []
            # if q.size() > 100:
            #     return []

            # if q.next():
            #     idhito = q.value("idhito")

            curTarea = qsatype.FLSqlCursor(u"gt_tareas")
            curTarea.setModeAccess(curTarea.Insert)
            curTarea.refreshBuffer()
            curTarea.setActivatedBufferCommited(True)
            curTarea.setValueBuffer(u"idproyecto", oParam["project"])
            curTarea.setValueBuffer(u"codestado", oParam["state"])
            curTarea.setValueBuffer(u"nombre", oParam["name"])
            curTarea.setValueBuffer(u"idusuario", oParam["person"])
            curTarea.setValueBuffer(u"descripcion", oParam["description"])
            curTarea.setValueBuffer(u"resuelta", False)
            curTarea.setValueBuffer(u"idhito", oParam["idhito"])
            if oParam["date"] and oParam["date"] != u"undefined":
                curTarea.setValueBuffer(u"fechavencimiento", oParam["date"])

            if not curTarea.commitBuffer():
                response["result"] = False
                response["error"] = "Error en commit"
            else:
                response["result"] = True
                response["ok"] = "Tarea creada"
        else:
            response["result"] = False
            response["error"] = "Error en autenticación"
        response["username"] = usuario
        nombreProyecto = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"nombre", ustr(u"idproyecto = '", oParam["project"], u"'"))
        response["nombreTarea"] = oParam["name"]
        response["nombreProyecto"] = nombreProyecto
        response["urlTarea"] = "https://app.dailyjob.io/gesttare/gt_tareas/" + str(curTarea.valueBuffer("idtarea"))
        return response

    def gesttare_createinbox(self, oParam):
        response = {}
        if "person" not in oParam or not oParam["person"]:
            usuario = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idusuario", ustr(u"email = '", str(oParam["email"]), u"'"))
            if not usuario:
                response["result"] = False
                response["error"] = "No existe el usuario de dailyjob, por tanto no tienes permisos para crear posibles tareas"
                response["username"] = oParam["email"]
                return response
        else:
            usuario = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idusuario", ustr(u"UPPER(usuario) = '", oParam["person"].upper(), u"'"))
        if not usuario:
            response["result"] = False
            response["error"] = "No existe el usuario de dailyjob, por tanto no tienes permisos para crear posibles tareas"
            response["username"] = oParam["email"]
            return response

        if oParam["appid"] == "23553220-e1b3-4592-a5de-fb41a08c60c8":
            response = {}
            descripcion = ""
            if "description" in oParam:
                descripcion = oParam["description"]
            curActualiz = qsatype.FLSqlCursor(u"gt_actualizaciones")
            curActualiz.setModeAccess(curActualiz.Insert)
            curActualiz.refreshBuffer()
            curActualiz.setValueBuffer(u"tipo", "inbox")
            curActualiz.setValueBuffer(u"tipobjeto", descripcion)
            curActualiz.setValueBuffer(u"otros", oParam["name"])
            curActualiz.setValueBuffer(u"fecha", datetime.date.today())
            curActualiz.setValueBuffer(u"hora", time.strftime('%H:%M:%S'))
            curActualiz.setValueBuffer(u"idusuarioorigen", usuario)
            if not curActualiz.commitBuffer():
                response["result"] = False
                response["error"] = "Error en commit"
            else:
                response["result"] = True
                response["ok"] = "Tarea creada"
            if not qsatype.FLUtil.sqlInsert(u"gt_actualizusuario", qsatype.Array([u"idactualizacion", u"idusuario", u"revisada"]), qsatype.Array([curActualiz.valueBuffer("idactualizacion"), usuario, False])):
                response["result"] = False
                response["error"] = "Error en commit"
        else:
            response["result"] = False
            response["error"] = "Error en autenticación"
        response["username"] = usuario
        return response

    def gesttare_actNuevoPartic(self, oParam, cursor):
        response = {}
        if "idusuario" not in oParam:
            # idUsuario = cursor.valueBuffer("idusuario")
            qryUsuarios = qsatype.FLSqlQuery()
            usuario = qsatype.FLUtil.nameUser()
            # qryUsuarios.setTablesList(u"aqn_user")
            # qryUsuarios.setSelect(u"idusuario, nombre")
            # qryUsuarios.setFrom(ustr(u"aqn_user"))
            # qryUsuarios.setWhere(ustr(u"1 = 1"))
            qryUsuarios.setTablesList(u"gt_partictarea, aqn_user")
            qryUsuarios.setSelect(u"DISTINCT(p.idusuario), u.usuario, u.nombre")
            qryUsuarios.setFrom(u"gt_partictarea p INNER JOIN aqn_user u ON p.idusuario = u.idusuario")
            qryUsuarios.setWhere(u"p.idtarea in (select p.idtarea from gt_partictarea p INNER JOIN aqn_user u  ON p.idusuario = u.idusuario where p.idusuario = '" + str(usuario) + "')")
            if not qryUsuarios.exec_():
                return False

            opts = []
            while qryUsuarios.next():
                tengousuario = qsatype.FLUtil.sqlSelect(u"gt_partictarea", u"idusuario", ustr(u"idusuario = '", qryUsuarios.value("idusuario"), u"' AND idtarea = '", cursor.valueBuffer("idtarea"), "'"))
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
                    "rel": "gt_tareas",
                    "calculatepk": False,
                    "style": {
                        "width": "100%"
                    },
                    "tipo": 180,
                    "verbose_name": "Participantes",
                    "label": "Participantes",
                    "key": "idusuario",
                    "function": "getParticipantesProyecto",
                    "desc": "usuario",
                    "validaciones": None,
                    "required": False,
                    "opts": opts
                }
            ]
            if not qsatype.FLUtil.sqlUpdate("gt_tareas", "ultimamodificacion", qsatype.Date().toString()[:10], "idtarea = " + str(cursor.valueBuffer("idtarea"))):
                return False
            return response
        else:
            participantes = json.loads(oParam["idusuario"])
            for p in participantes:
                curPartic = qsatype.FLSqlCursor("gt_partictarea")
                curPartic.select(ustr("idusuario = '", p, "' AND idtarea = '", cursor.valueBuffer("idtarea"), "'"))
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
                        curPartic.setValueBuffer("idtarea", cursor.valueBuffer("idtarea"))
                        if not curPartic.commitBuffer():
                            return False
            response = {}
            response["resul"] = True
            response["msg"] = "Actualizados los participantes"
            return response

    def gesttare_bChCursor(self, fN, cursor):
        # if not qsatype.FactoriaModulos.get('formRecordgt_tareas').iface.bChCursor(fN, cursor):
        #     return False
        if fN == "idproyecto":
            cursor.setNull("idhito")
            numHitos = qsatype.FLUtil.sqlSelect(u"gt_hitosproyecto", u"COUNT(idhito)", ustr(u"idproyecto = '", cursor.valueBuffer("idproyecto"), u"' AND resuelta = false"))
            if numHitos == 1:
                cursor.setValueBuffer("idhito", qsatype.FLUtil.sqlSelect(u"gt_hitosproyecto", u"idhito", ustr(u"idproyecto = '", cursor.valueBuffer("idproyecto"), u"' AND resuelta = false")))
            elif numHitos == 0:
                qsatype.FLUtil.ponMsgError("No es posible crear tareas para este proyecto, no tiene hitos activos")
        if fN == "idusuario":
            curPartic = qsatype.FLSqlCursor("gt_partictarea")
            curPartic.select(ustr("idusuario = '", cursor.valueBuffer("idusuario"), "' AND idtarea = '", cursor.valueBuffer("idtarea"), "'"))
            curPartic.refreshBuffer()
            if not curPartic.first():
                curPartic.setModeAccess(curPartic.Insert)
                curPartic.refreshBuffer()
                curPartic.setValueBuffer("idusuario", cursor.valueBuffer("idusuario"))
                curPartic.setValueBuffer("idtarea", cursor.valueBuffer("idtarea"))
                if not curPartic.commitBuffer():
                    return False
        if fN == "idhito":
            cursor.setValueBuffer("fechaentrega", qsatype.FLUtil.sqlSelect(u"gt_hitosproyecto", u"fechaterminado", ustr(u"idhito = '", cursor.valueBuffer("idhito"), u"'")))

        return True

    def gesttare_getFilters(self, model, name, template=None):
        filters = []
        usuario = qsatype.FLUtil.nameUser()
        if name == "renegociarusuario":
            proin = []
            # curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
            # curProyectos.select("idusuario = '" + str(usuario) + "'")
            # while curProyectos.next():
            #     curProyectos.setModeAccess(curProyectos.Browse)
            #     curProyectos.refreshBuffer()
            #     proin.append(curProyectos.valueBuffer("idproyecto"))
            q = qsatype.FLSqlQuery()
            q.setTablesList(u"gt_proyectos, gt_particproyecto")
            q.setSelect(u"t.idproyecto")
            q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.idproyecto=p.idproyecto")
            q.setWhere(u"p.idusuario = '" + usuario + "' AND  t.archivado = false")

            if not q.exec_():
                return []
            if q.size() > 100:
                return []

            while q.next():
                proin.append(q.value("idproyecto"))
            return [{'criterio': 'idusuario__exact', 'valor': usuario}, {'criterio': 'fechavencimiento__lt', 'valor': str(qsatype.Date().toString()[:10])}, {'criterio': 'idproyecto__in', 'valor': proin, 'tipo': 'q'}]

        if name == "renegociarusuarioespera":
            # proin = []
            # # curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
            # # curProyectos.select("idusuario = '" + str(usuario) + "'")
            # # while curProyectos.next():
            # #     curProyectos.setModeAccess(curProyectos.Browse)
            # #     curProyectos.refreshBuffer()
            # #     proin.append(curProyectos.valueBuffer("idproyecto"))
            # q = qsatype.FLSqlQuery()
            # q.setTablesList(u"gt_proyectos, gt_particproyecto")
            # q.setSelect(u"t.idproyecto")
            # q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.idproyecto=p.idproyecto")
            # q.setWhere(u"p.idusuario = '" + usuario + "' AND  t.archivado = false")

            # if not q.exec_():
            #     return []
            # if q.size() > 100:
            #     return []

            # while q.next():
            #     proin.append(q.value("idproyecto"))

            valores = flgesttare_def.iface.revisar_indicadores(usuario)
            tain = []
            if "idtarea" in valores and valores["idtarea"]:
                for e in valores["idtarea"]:
                    tain.append(e)
            return [{'criterio': 'idusuario__exact', 'valor': usuario}, {'criterio': 'idtarea__in', 'valor': tain, 'tipo': 'q'}, {'criterio': 'codestado__exact', 'valor': "En espera"}]

        

        if name == "renegociarusuariotreinta":
            proin = []
            # # curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
            # # curProyectos.select("idusuario = '" + str(usuario) + "'")
            # # while curProyectos.next():
            # #     curProyectos.setModeAccess(curProyectos.Browse)
            # #     curProyectos.refreshBuffer()
            # #     proin.append(curProyectos.valueBuffer("idproyecto")),
            # q = qsatype.FLSqlQuery()
            # q.setTablesList(u"gt_proyectos, gt_particproyecto")
            # q.setSelect(u"t.idproyecto")
            # q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.idproyecto=p.idproyecto")
            # q.setWhere(u"p.idusuario = '" + usuario + "' AND  t.archivado = false")

            # if not q.exec_():
            #     return []
            # if q.size() > 100:
            #     return []

            # while q.next():
            #     proin.append(q.value("idproyecto"))

            valores = flgesttare_def.iface.revisar_indicadores(usuario)
            tain = []
            if "idtarea_planear" in valores and valores["idtarea_planear"]:
                for e in valores["idtarea_planear"]:
                    tain.append(e)

            return [{'criterio': 'idusuario__exact', 'valor': usuario}, {'criterio': 'idtarea__in', 'valor': tain, 'tipo': 'q'}]

        if name == 'proyectosusuario':
            # proin = "("
            proin = []
            # curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
            # curProyectos.select("idusuario = '" + str(usuario) + "'")
            # while curProyectos.next():
            #     curProyectos.setModeAccess(curProyectos.Browse)
            #     curProyectos.refreshBuffer()
            #     proin.append(curProyectos.valueBuffer("idproyecto"))
            q = qsatype.FLSqlQuery()
            q.setTablesList(u"gt_proyectos, gt_particproyecto")
            q.setSelect(u"t.idproyecto")
            q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.idproyecto=p.idproyecto")
            q.setWhere(u"p.idusuario = '" + usuario + "' AND  t.archivado = false AND (p.tipo <> 'observador' OR p.tipo is null)")

            if not q.exec_():
                return []
            if q.size() > 100:
                return []

            while q.next():
                proin.append(q.value("idproyecto"))


            tain = []
            qt = qsatype.FLSqlQuery()
            qt.setTablesList(u"gt_tareas, gt_proyectos, gt_particproyecto, gt_partictarea")
            qt.setSelect(u"gt_partictarea.idtarea")
            qt.setFrom(u"gt_partictarea INNER JOIN gt_tareas ON gt_partictarea.idtarea = gt_tareas.idtarea INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto INNER JOIN gt_particproyecto ON gt_proyectos.idproyecto = gt_particproyecto.idproyecto")
            qt.setWhere(u"gt_partictarea.idusuario = '" + usuario + "' AND gt_particproyecto.idusuario = '" + usuario + "' AND  gt_proyectos.archivado = false AND gt_particproyecto.tipo = 'observador'")
            if not qt.exec_():
                return []
            if qt.size() > 100:
                return []

            while qt.next():
                tain.append(qt.value("idtarea"))

    
            return [{'criterio': 'idproyecto__in', 'valor': proin, 'tipo': 'q'}, {'criterio': 'idtarea__in', 'valor': tain, 'tipo': 'q'}]
        return filters

    def gesttare_getTareasUsuario(self, oParam):
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_tareas, gt_particproyecto")
        q.setSelect(u"t.idtarea, t.nombre, p.idproyecto")
        q.setFrom(u"gt_tareas t LEFT JOIN gt_particproyecto p ON t.idproyecto=p.idproyecto")
        q.setWhere(u"p.idusuario = '" + qsatype.FLUtil.nameUser() + "' AND UPPER(t.nombre) LIKE UPPER('%" + oParam["val"] + "%')  ORDER BY t.nombre LIMIT 7")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 100:
            print("sale por aqui")
            return []

        while q.next():
            # descripcion = str(q.value(2)) + "€ " + q.value(1)
            data.append({"idtarea": q.value(0), "nombre": q.value(1)})

        return data

    def gesttare_check_permissions(self, model, prefix, pk, template, acl, accion):
        if template == "formRecord":
            curTarea = qsatype.FLSqlCursor("gt_tareas")
            curTarea.select(ustr("idtarea = '", pk, "'"))
            curTarea.refreshBuffer()
            if curTarea.first():
                curTarea.setModeAccess(curTarea.Browse)
                curTarea.refreshBuffer()
                idproyecto = curTarea.valueBuffer("idproyecto")
                nombreUsuario = qsatype.FLUtil.nameUser()
                pertenece = qsatype.FLUtil.sqlSelect(u"gt_particproyecto", u"idusuario", ustr(u"idusuario = '", nombreUsuario, u"' AND idproyecto = '", idproyecto, "'"))
                if not pertenece:
                    return False
            else:
                return False

        # if accion == "delete":
        #     nombreUsuario = qsatype.FLUtil.nameUser()
        #     idcompanyUser = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", u"idusuario = '" + nombreUsuario + u"'")
        #     idcompanyProject = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"idcompany", ustr(u" idproyecto = '", pk, "'"))
        #     if idcompanyUser != idcompanyProject:
        #         return False
        return True

    def gesttare_borrar_tarea(self, model, oParam, cursor):
        resul = {}
        if "confirmacion" in oParam and oParam["confirmacion"]:
            cursor.setModeAccess(cursor.Del)
            cursor.refreshBuffer()
            if not cursor.commitBuffer():
                return False
            resul["return_data"] = False
            resul["msg"] = "Tarea eliminada"
            return resul
        resul['status'] = 2
        resul['confirm'] = "La tarea será eliminada"
        return resul

    def gesttare_gotoGestionarTiempo(self, model, cursor):
        tengopermiso = flgesttare_def.iface.compruebaPermisosPlan("startstop")
        # response = self.plan_compania(user_name)
        if tengopermiso != True:
            return tengopermiso
        return "/gesttare/gt_timetracking/newRecord?p_idtarea=" + str(cursor.valueBuffer("idtarea"))

    def gesttare_commonCalculateField(self, fN=None, cursor=None):
        valor = None

        if fN == u"hdedicadas":
            valor = qsatype.FLUtil.quickSqlSelect("gt_timetracking", "SUM(totaltiempo)", "idtarea = {}".format(cursor.valueBuffer("idtarea"))) or 0
            if valor != 0:
                valor = valor.total_seconds()
        return valor

    def gesttare_verTrackingTarea(self, cursor):
        response = {}
        response["url"] = "/gesttare/gt_timetracking/master"
        response["prefix"] = "mastertimetracking"
        response["filter"] = '{"tarea": "' + str(cursor.valueBuffer("nombre")) + '"}'
        return response

    def gesttare_gotoTarea(self, model):
        url = '/gesttare/gt_tareas/' + str(model.idtarea) 
        return url

    def gesttare_queryGrid_renegociacion(self, model):
        usuario = qsatype.FLUtil.nameUser()
        query = {}
        query["tablesList"] = ("gt_tareas")
        query["select"] = ("gt_tareas.idtarea, gt_tareas.idproyecto, gt_tareas.codestado, gt_tareas.idusuario, gt_tareas.fechavencimiento, gt_tareas.fechaentrega, gt_tareas.nombre")
        # query["select"] = ("gt_tareas.idtarea, gt_tareas.fechainicio, gt_tareas.descripcion")
        query["from"] = ("gt_tareas")
        query["where"] = ("gt_tareas.idusuario = '" + str(usuario)  + "' AND gt_tareas.resuelta = false AND (gt_tareas.fechavencimiento < '" + qsatype.Date().toString()[:10] + "' OR gt_tareas.fechaentrega < '" + qsatype.Date().toString()[:10] + "')")
        query["orderby"] = ("gt_tareas.fechavencimiento, gt_tareas.fechavencimiento")
        query["limit"] = 50
        return query
        

    def gesttare_queryGrid_revisionTareas(self, model):
        usuario = qsatype.FLUtil.nameUser()
        valores = flgesttare_def.iface.revisar_indicadores(usuario)
        tain = "("
        if "idtarea" in valores and valores["idtarea"]:
            for e in valores["idtarea"]:
                tain = tain + "" + str(e) + ", "
        tain = tain + " null)"
        where_filter = "(gt_tareas.idtarea IN " + tain + " OR gt_tareas.idtarea IS NULL)"
        query = {}
        query["tablesList"] = ("gt_tareas")
        query["select"] = ("gt_tareas.idtarea, gt_tareas.nombre, gt_proyectos.nombre, gt_tareas.fechavencimiento, gt_tareas.fechaentrega, gt_tareas.codestado")
        query["from"] = ("gt_tareas INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto")
        query["where"] = where_filter
        query["orderby"] = ("gt_tareas.fechavencimiento")
        query["limit"] = 50
        return query

    def gesttare_queryGrid_revisionTareasTreinta(self, model):
        usuario = qsatype.FLUtil.nameUser()
        valores = flgesttare_def.iface.revisar_indicadores(usuario)
        tain = "("
        if "idtarea_planear" in valores and valores["idtarea_planear"]:
            for e in valores["idtarea_planear"]:
                tain = tain + "" + str(e) + ", "
        tain = tain + " null)"
        where_filter = "(gt_tareas.idtarea IN " + tain + " OR gt_tareas.idtarea IS NULL)"
        query = {}
        query["tablesList"] = ("gt_tareas")
        query["select"] = ("gt_tareas.idtarea, gt_tareas.nombre, gt_proyectos.nombre, gt_tareas.fechavencimiento, gt_tareas.fechaentrega, gt_tareas.codestado")
        query["from"] = ("gt_tareas INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto")
        query["where"] = where_filter
        query["orderby"] = ("gt_tareas.fechavencimiento")
        query["limit"] = 50
        return query

    def gesttare_getParticipantesProyecto(self, model, oParam):
        data = []
        usuario = qsatype.FLUtil.nameUser()
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_tareas, gt_particproyecto, aqn_user")
        q.setSelect(u"p.idusuario, u.usuario")
        q.setFrom(u"gt_tareas t LEFT JOIN gt_particproyecto p ON t.idproyecto=p.idproyecto INNER JOIN aqn_user u ON u.idusuario =p.idusuario")
        q.setWhere(u"t.idtarea = '" + str(model.idtarea) + "' AND UPPER(u.nombre) LIKE UPPER('%" + oParam["val"] + "%') ORDER BY u.usuario LIMIT 7")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 100:
            print("sale por aqui")
            return []

        while q.next():
            # descripcion = str(q.value(2)) + "€ " + q.value(1)
            data.append({"idusuario": q.value(0), "usuario": q.value(1)})
        return data

    def gesttare_gotoNewRecordAnotacion(self, oParam):
        if "nombre" not in oParam:
            response = {}
            response['status'] = -1
            response['data'] = {}
            response["prefix"] = "gt_tareas"
            response["title"] = "Crear nueva tarea"
            response["serverAction"] = "gotoNewRecordAnotacion"
            response["customButtons"] = [{"accion": "serverAction","nombre": "Crear posible tarea", "serverAction": "gotoNewRecordAnotacion", "className": "creaAnotacionButton"}, {"accion": "serverAction", "pk": "NF", "nombre": "Ir a completar tarea >", "serverAction": "gotonewrecordtarea", "className": "anotacionToTareaButton"}]
            if "abierto" in oParam:
                response["error"] = "El campo nombre es obligatorio"
            response['params'] = [
                {
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "tipo": 3,
                    "verbose_name": "Nombre",
                    "key": "nombre",
                    "validaciones": None,
                    "maxlength": 200,
                    "required": True
                },
                {
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "tipo": 3,
                    "verbose_name": "Descripción",
                    "key": "descripcion",
                    "validaciones": None,
                    "required": False
                },
                {
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "tipo": 3,
                    "verbose_name": "Nombre",
                    "key": "abierto",
                    "validaciones": None,
                    "required": False,
                    "visible": False,
                    "value": "True"
                }
            ]
            return response
        else:
            if "nombre" in oParam:
                response = {}
                descripcion = ""
                if "descripcion" in oParam:
                    descripcion = oParam["descripcion"]
                idUsuario = qsatype.FLUtil.nameUser()
                curActualiz = qsatype.FLSqlCursor(u"gt_actualizaciones")
                curActualiz.setModeAccess(curActualiz.Insert)
                curActualiz.refreshBuffer()
                curActualiz.setValueBuffer(u"tipo", "anotacion")
                curActualiz.setValueBuffer(u"tipobjeto", descripcion)
                curActualiz.setValueBuffer(u"otros", oParam["nombre"])
                curActualiz.setValueBuffer(u"fecha", datetime.date.today())
                curActualiz.setValueBuffer(u"hora", time.strftime('%H:%M:%S'))
                curActualiz.setValueBuffer(u"idusuarioorigen", idUsuario)
                if not curActualiz.commitBuffer():
                    return False
                if not qsatype.FLUtil.sqlInsert(u"gt_actualizusuario", qsatype.Array([u"idactualizacion", u"idusuario", u"revisada"]), qsatype.Array([curActualiz.valueBuffer("idactualizacion"), idUsuario, False])):
                    return False
                response["msg"] = "Posible tarea creada"
                return response;

        return True


    def gesttare_gotonewrecordtarea(self, oParam):
        # if "nombre" not in oParam:
        #     response = {}
        #     response['status'] = -1
        #     response['data'] = {}
        #     response["prefix"] = "gt_tareas"
        #     response["title"] = "Crear nueva tarea"
        #     response["serverAction"] = "gotoNewRecordAnotacion"
        #     response["customButtons"] = [{"accion": "serverAction","nombre": "Crear posible tarea", "serverAction": "gotoNewRecordAnotacion", "className": "creaAnotacionButton"}, {"accion": "serverAction","nombre": "Ir a completar tarea >", "serverAction": "gotonewrecordtarea", "className": "anotacionToTareaButton"}]
        #     response['params'] = [
        #         {
        #             "componente": "YBFieldDB",
        #             "prefix": "otros",
        #             "tipo": 3,
        #             "verbose_name": "Nombre",
        #             "key": "nombre",
        #             "validaciones": None,
        #             "required": True
        #         },
        #         {
        #             "componente": "YBFieldDB",
        #             "prefix": "otros",
        #             "tipo": 3,
        #             "verbose_name": "Descripción",
        #             "key": "descripcion",
        #             "validaciones": None,
        #             "required": False
        #         }
        #     ]
        #     return response
        # else:
        usuario = qsatype.FLUtil.nameUser()
        response = {}
        curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
        curProyectos.select("idusuario = '" + str(usuario) + "'")
        if not curProyectos.first():
            response["status"] = 1
            response["msg"] = "Debes participar en un proyecto para anotar tareas"
            return response
        params = ""
        if "nombre" in oParam:
            params += "?p_nombre=" + urllib.parse.quote(str(oParam["nombre"]))
            if "descripcion" in oParam:
                params += "&p_descripcion=" + urllib.parse.quote(str(oParam["descripcion"]))
        response["url"] = '/gesttare/gt_tareas/newRecord' + params
        return response

    def gesttare_drawif_checkAdjuntos(self, cursor):
        # if cursor.valueBuffer("resuelta") == True:
        if cursor.valueBuffer("idactualizacion"):
            adjunto = qsatype.FLUtil.quickSqlSelect("gd_objetosdoc", "clave", "clave = '{}'".format(cursor.valueBuffer("idactualizacion")))
            if adjunto:
                return True
        return "hidden"

    def gesttare_drawif_checkActu2(self, cursor):
        if cursor.valueBuffer("idactualizacion") != None:
            return True
        return "hidden"

    def gesttare_drawif_checkNormal(self, cursor):
        if cursor.valueBuffer("idactualizacion"):
            return "hidden"
        return True

    def gesttare_drawif_completartarea(self, cursor):
        if cursor.valueBuffer("resuelta") == True:
            return "hidden"

    def gesttare_drawif_abrirtarea(self, cursor):
        if cursor.valueBuffer("resuelta") == False:
            return "hidden"

    def gesttare_drawif_iniciartarea(self, cursor):
        user_name = qsatype.FLUtil.nameUser()

        tareaactiva = qsatype.FLUtil.quickSqlSelect("aqn_user", "idtareaactiva", "idusuario = '{}'".format(user_name))

        if tareaactiva == cursor.valueBuffer("idtarea"):
            return "hidden"

    def gesttare_drawif_parartarea(self, cursor):
        user_name = qsatype.FLUtil.nameUser()
        
        tareaactiva = qsatype.FLUtil.quickSqlSelect("aqn_user", "idtareaactiva", "idusuario = '{}'".format(user_name))

        if tareaactiva != cursor.valueBuffer("idtarea"):
            return "hidden"

    def gesttare_iniciaValoresCursor(self, cursor=None):
        # usuario = qsatype.FLUtil.nameUser()
        hoy = qsatype.Date()
        fechacreacion = str(hoy)[:10]
        cursor.setValueBuffer("codestado", "Por Hacer")
        cursor.setValueBuffer("fechacreacion", fechacreacion)
        cursor.setValueBuffer("ultimamodificacion", fechacreacion)
        if cursor.valueBuffer("idactualizacion"):
            nombre = cursor.valueBuffer("nombre")
            idactualizacion = cursor.valueBuffer("idactualizacion")
            nombre = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones", "otros", "idactualizacion = {}".format(idactualizacion)) or None
            descripcion = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones", "tipobjeto", "idactualizacion = {}".format(idactualizacion)) or None
            cursor.setValueBuffer("nombre", nombre)
            cursor.setValueBuffer("descripcion", descripcion)
            cursor.setValueBuffer("idactualizacion", idactualizacion)
        return True

    def gesttare_verTarea(self, model, cursor):
        url = "/gesttare/gt_tareas/" + str(cursor.valueBuffer("idtarea"))
        return url

    def gesttare_validateCursor(self, cursor):
        msg = ""
        # if not cursor.valueBuffer("nombre"):
        #     msg += "El campo Nombre no puede ser nulo <br/><br/>"
        error = False

        user_name = qsatype.FLUtil.nameUser()
        
        fecha_entrega_activa = qsatype.FLUtil.quickSqlSelect("aqn_user", "fentregaobligatoria", "idusuario = {}".format(str(user_name)))
        nomenclatura_activa = qsatype.FLUtil.quickSqlSelect("aqn_user", "nomenclatura", "idusuario = {}".format(str(user_name)))
        if not cursor.valueBuffer("idproyecto"):
            msg += "El campo Proyecto no puede estar vacío<br/><br/>"
            error = True

        if not cursor.valueBuffer("idhito"):
            msg += "El campo Hito no puede estar vacío<br/><br/>"
            error = True
        if fecha_entrega_activa:
            if not cursor.valueBuffer("fechaentrega"):
                msg += "El campo Fecha de entrega no puede estar vacío<br/><br/>"
                error = True

            elif cursor.valueBuffer("fechaentrega"):
                hito_fechat = qsatype.FLUtil.quickSqlSelect("gt_hitosproyecto", "fechaterminado", "idhito = {}".format(cursor.valueBuffer("idhito"))) or None 
                if hito_fechat:
                    if str(hito_fechat) < cursor.valueBuffer("fechaentrega"):
                        msg += "La Fecha de entrega no puede ser superior que la fecha de terminado del hito. Selecciona una fecha anterior o igual a esa fecha, o modifica la fecha de finalización del hito pulsando <a href='http://127.0.0.1:8000/gesttare/gt_hitosproyecto/{}' target='_blank'>aquí</a><br/><br/>".format(cursor.valueBuffer("idhito"))
                        error = True

        if nomenclatura_activa:
            if cursor.modeAccess() == cursor.Insert and cursor.valueBuffer("nombre"):
                nombre = cursor.valueBuffer("nombre")
                valor = nombre.upper()
                valor = valor.strip()
                if nombre[0] == "#":
                    if " " in nombre:
                        valor = valor.split(" ", 1)
                        valor = valor[1].split(" ", 1)
                        if valor[0][-2:] != "AR" and valor[0][-2:] != "ER" and valor[0][-2:] != "IR":
                            # qsatype.FLUtil.ponMsgError(msg + "Las tareas deben empezar por verbo en infinitivo")
                            msg += "Las tareas deben empezar por verbo en infinitivo"
                            error = True
                            # return False
                    else:
                        msg += "Además del hashtag, debes establecer un nombre para la tarea"
                        error = True

                else:
                    if " " in valor:
                        valor = valor.split(" ", 1)
                        if valor[0][-2:] != "AR" and valor[0][-2:] != "ER" and valor[0][-2:] != "IR":
                            # qsatype.FLUtil.ponMsgError(msg + "Las tareas deben empezar por verbo en infinitivo")
                            msg += "Las tareas deben empezar por verbo en infinitivo"
                            error = True
                            # return False

                    else:
                        if valor[-2:] != "AR" and valor[-2:] != "ER" and valor[-2:] != "IR":
                            # qsatype.FLUtil.ponMsgError(msg + "Las tareas deben empezar por verbo en infinitivo")
                            msg += "Las tareas deben empezar por verbo en infinitivo"
                            error = True
                            # return False

        if not cursor.valueBuffer("nombre"):
            msg += "El campo Nombre no puede estar vacío"
            error = True


        # if not cursor.valueBuffer("nombre") or not cursor.valueBuffer("idproyecto") or not cursor.valueBuffer("idhito") or not cursor.valueBuffer("fechaentrega"):
            # qsatype.FLUtil.ponMsgError(msg)
            # return False

        if error:
            qsatype.FLUtil.ponMsgError(msg)
            return False
           
        return True


    def gesttare_gotomomentos(self):
        # response = {}
        # response["newtab"] = True
        # response["url"] = "http://doc.dailyjob.io/"
        # return response
        url = "https://doc.dailyjob.io/"
        return url
        

    def gesttare_gotoNewRecordRecordatorioAtrasada(self, oParam):
        response = {}
        if not oParam or "confirmacion" not in oParam:
            # valores = flgesttare_def.iface.revisar_indicadores(user_name)
            # # atrasada = qsatype.FLUtil.quickSqlSelect("gt_tareas t INNER JOIN gt_proyectos p ON t.idproyecto = p.idproyecto", "COUNT(t.idtarea)", "t.resuelta = false AND t.fechavencimiento < '{}' AND t.idusuario = '{}' AND p.archivado = false".format(str(qsatype.Date())[:10] ,usuario))
            # # if atrasada > 0:
            # if 'atrasadas' in valores and valores['atrasadas']:
            response["status"] = 2
            response["confirm"] = "Contar con tareas cuya fecha está atrasada te hace perder el control sobre la actividad pendiente, y puede evitar que acabes haciendo las tareas más prioritarias.</br></br> ¿Quieres renegociar ahora?"
            response["serverAction"] = "gotoNewRecordRecordatorioAtrasada"
            response["customButtons"] = [{"accion": "goto","nombre": "Sí", "url": "/gesttare/gt_tareas/custom/renegociar"}, {"accion": "cancel","nombre": "No"}]
            # response["goto"] = {"nombre": "Sí", "url": "/gesttare/gt_tareas/custom/renegociar"}
            return response

        return True

    def gesttare_gotoNewRecordRecordatorioBandeja(self, oParam):
        response = {}
        if not oParam or "confirmacion" not in oParam:
            # valores = flgesttare_def.iface.revisar_indicadores(user_name)
            # # atrasada = qsatype.FLUtil.quickSqlSelect("gt_tareas t INNER JOIN gt_proyectos p ON t.idproyecto = p.idproyecto", "COUNT(t.idtarea)", "t.resuelta = false AND t.fechavencimiento < '{}' AND t.idusuario = '{}' AND p.archivado = false".format(str(qsatype.Date())[:10] ,usuario))
            # # if atrasada > 0:
            # if 'atrasadas' in valores and valores['atrasadas']:
            response["status"] = 2
            response["confirm"] = "La bandeja de entrada es un punto de entrada de comunicaciones del resto del equipo. No revisarla con regularidad puede hacer perder la confianza del resto de personas sobre la lectura de lo que comentan o los cambios que hacen. </br> Si la comunicación no se canaliza por ahí, es posible que se creen otros medios alternativos que provoquen interrupciones innecesarias.</br></br> ¿Quieres revisar la bandeja de entrada?"
            response["serverAction"] = "gotoNewRecordRecordatorioBandeja"
            response["customButtons"] = [{"accion": "goto","nombre": "Sí", "url": "/gesttare/gt_actualizaciones/master"}, {"accion": "cancel","nombre": "No"}]
            # response["goto"] = {"nombre": "Sí", "url": "/gesttare/gt_tareas/custom/renegociar"}
            return response

        return True


    def gesttare_gotoNewRecordRecordatorioEspera(self, oParam):
        response = {}
        if not oParam or "confirmacion" not in oParam:
            # valores = flgesttare_def.iface.revisar_indicadores(user_name)
            # # atrasada = qsatype.FLUtil.quickSqlSelect("gt_tareas t INNER JOIN gt_proyectos p ON t.idproyecto = p.idproyecto", "COUNT(t.idtarea)", "t.resuelta = false AND t.fechavencimiento < '{}' AND t.idusuario = '{}' AND p.archivado = false".format(str(qsatype.Date())[:10] ,usuario))
            # # if atrasada > 0:
            # if 'atrasadas' in valores and valores['atrasadas']:
            response["status"] = 2
            response["confirm"] = 'Tienes tareas en "en espera" con más de 7 días sin revisión. ¿Quieres tomar alguna decisión con ellas?'
            response["serverAction"] = "gotoNewRecordRecordatorioBandejaEspera"
            response["customButtons"] = [{"accion": "goto","nombre": "Sí", "url": "/gesttare/gt_tareas/custom/recordatorio"}, {"accion": "cancel","nombre": "No"}]
            # response["goto"] = {"nombre": "Sí", "url": "/gesttare/gt_tareas/custom/renegociar"}
            return response

        return True


    def gesttare_gotoReturnActualizacion(self, oParam):
        response = {}

        if not oParam or "confirmacion" not in oParam:
            # valores = flgesttare_def.iface.revisar_indicadores(user_name)
            # # atrasada = qsatype.FLUtil.quickSqlSelect("gt_tareas t INNER JOIN gt_proyectos p ON t.idproyecto = p.idproyecto", "COUNT(t.idtarea)", "t.resuelta = false AND t.fechavencimiento < '{}' AND t.idusuario = '{}' AND p.archivado = false".format(str(qsatype.Date())[:10] ,usuario))
            # # if atrasada > 0:
            # if 'atrasadas' in valores and valores['atrasadas']:
            response["status"] = 2
            response["confirm"] = "La tarea no ha sido guardada, si continuas perderás la información. </br></br> ¿Quieres salir de la página?"
            response["serverAction"] = "gotoReturnActualizacion"
            response["customButtons"] = [{"accion": "goto","nombre": "Sí", "url": "/gesttare/gt_actualizaciones/master"}]
            # response["goto"] = {"nombre": "Sí", "url": "/gesttare/gt_tareas/custom/renegociar"}
            return response

        return True


    def gesttare_opciones_recordatorio(self, oParam):
        user_name = qsatype.FLUtil.nameUser()
        valores = flgesttare_def.iface.revisar_indicadores(user_name)
        # msgp = []
        msg = []
        botones = []
        clase = []
        titulo_acordeon = []
        response = {}
        if 'atrasadas' in valores and valores['atrasadas']:
            clase.append("atrasada")
            # msg.append("<strong>CONSEJO: </strong> Contar con tareas cuya fecha está atrasada te hace perder el control sobre la actividad pendiente, y puede evitar que acabes haciendo las tareas más prioritarias.")
            msg.append("<img src='/static/dist/img/icons/diagrama-tareas-atrasadas.svg' style='width:600px; height:300px; margin-top:-30px; margin-left:auto; margin-right:auto; display:block; margin-bottom:-60px;'></img><br/> <a href='http://doc.dailyjob.io/books/manual-de-usuario/page/posponer-y-renegociar-las-tareas' class='btn btn-primary btn-submit modal-btn' target='_blank'>Aprender más</a>")
            # msgp.append("¿Quieres renegociar ahora?")
            if valores['atrasadas'] > 1:
                nombre = "Tienes {} tareas atrasadas".format(valores['atrasadas'])
            else:
                nombre = "Tienes {} tarea atrasada".format(valores['atrasadas'])
            titulo_acordeon.append(nombre)
            botones.append({"accion": "goto","nombre": "Renegociar tareas", "url": "/gesttare/gt_tareas/custom/renegociar"})

        if 'revisada' in valores and valores['revisada']:
            clase.append("revisada")
            # msg.append("<strong>CONSEJO: </strong>La bandeja de entrada es un punto de entrada de comunicaciones del resto del equipo. No revisarla con regularidad puede hacer perder la confianza del resto de personas sobre la lectura de lo que comentan o los cambios que hacen. <br/>Si la comunicación no se canaliza por ahí, es posible que se creen otros medios alternativos que provoquen interrupciones innecesarias.")
            # msgp.append("¿Quieres revisar la bandeja de entrada?")
            msg.append("<img src='/static/dist/img/icons/diagrama-tareas-bandeja-entrada.svg' style='width:600px; height:300px; margin-top:-30px; margin-left:auto; margin-right:auto; display:block; margin-bottom:-60px;'></img><br/> <a href='http://doc.dailyjob.io/books/manual-de-usuario/page/revisi%C3%B3n-de-la-bandeja-de-entrada' class='btn btn-primary btn-submit modal-btn' target='_blank'>Aprender más</a>")
            if valores['revisada'] > 1:
                nombre = "Tienes {} notificaciones sin revisar".format(valores['revisada'])
            else:
                nombre = "Tienes {} notificación sin revisar".format(valores['revisada'])
            titulo_acordeon.append(nombre)
            botones.append({"accion": "goto","nombre": "Revisar bandeja", "url": "/gesttare/gt_actualizaciones/master"})

        if "espera_sin" in valores and valores["espera_sin"]:
            clase.append("espera_sin")
            # msg.append('<strong>CONSEJO: </strong>Establecemos el estado "en espera" para indicar que esa tarea sobre la que tenemos responsabilidad está pendiente de una tercera persona, normalmente externa al equipo. <br/> <br/> El objetivo es hacer seguimiento regular a estas tareas para determinar si reclamamos, esperamos, retomamos o completamos.<br/> <br/> Te animamos revises las tareas en estado "en espera" y que añadas comentarios sobre tu estado de modo que veas el histórico de su seguimiento.')
            msg.append("<img src='/static/dist/img/icons/diagrama-tareas-en-espera.svg' style='width:600px; height:300px; margin-top:-30px; margin-left:auto; margin-right:auto; display:block; margin-bottom:-60px;'></img> <br/> <a href='javascript:void(0)' class='btn btn-primary btn-submit modal-btn' target='_blank'>Aprender más</a>")
            # msgp.append("¿Quieres tomar alguna decisión con ellas?")
            # response["atrasadas"] = "espera_sin"
            if valores["espera_sin"] > 1:
                nombre = "Tienes {} tareas en espera sin revisar".format(valores['espera_sin'])
            else:
                nombre = "Tienes {} tarea en espera sin revisar".format(valores['espera_sin'])
            titulo_acordeon.append(nombre)
            botones.append({"accion": "goto","nombre": "Revisar tareas", "url": "/gesttare/gt_tareas/custom/recordatorio"})

        if 'atrasadas' not in valores and 'revisada' not in valores and "espera_sin" not in valores:
            response["resul"] = True
            response["msg"] = "No tienes alertas en el momento producir"
            return response

        response['status'] = 4
        response['data'] = {}
        response["clase"] = clase
        response["titulo_acordeon"] = titulo_acordeon
        response["msg"]= msg
        # response["msgp"]= msgp
        response["prefix"] = "gt_tareas"
        response["title"] = "Alertas del Momento Producir"
        response["serverAction"] = "opciones_recordatorio"
        response["customButtons"] = botones
        
        response['params'] = [
            
        ]

        
        return response


    def gesttare_opciones_recordatorio_anotar(self, oParam):
        user_name = qsatype.FLUtil.nameUser()
        valores = flgesttare_def.iface.revisar_indicadores(user_name)
        # msgp = []
        msg = []
        botones = []
        clase = []
        titulo_acordeon = []
        response = {}
        if 'revisada_anotar' in valores and valores['revisada_anotar']:
            clase.append("revisada_anotar")
            # msg.append("<strong>CONSEJO: </strong>La bandeja de entrada es un punto de entrada de comunicaciones del resto del equipo. No revisarla con regularidad puede hacer perder la confianza del resto de personas sobre la lectura de lo que comentan o los cambios que hacen. <br/>Si la comunicación no se canaliza por ahí, es posible que se creen otros medios alternativos que provoquen interrupciones innecesarias.")
            # msgp.append("¿Quieres revisar la bandeja de entrada?")
            msg.append("<img src='/static/dist/img/icons/diagrama-tareas-posibles-tareas.svg' style='width:600px; height:300px; margin-top:-30px; margin-left:auto; margin-right:auto; display:block; margin-bottom:-60px;'></img><br/> <a href='http://doc.dailyjob.io/books/manual-de-usuario/page/anotar-tareas' class='btn btn-primary btn-submit modal-btn' target='_blank'>Aprender más</a>")
            if valores['revisada_anotar'] > 1:
                nombre = "Tienes {} posibles tareas sin revisar".format(valores['revisada_anotar'])
            else:
                nombre = "Tienes {} posible tarea sin revisar".format(valores['revisada_anotar'])
            titulo_acordeon.append(nombre)
            botones.append({"accion": "goto","nombre": "Ver posibles tareas", "url": "/gesttare/gt_actualizaciones/master"})

            response['status'] = 4
            response['data'] = {}
            response["clase"] = clase
            response["titulo_acordeon"] = titulo_acordeon
            response["msg"]= msg
            # response["msgp"]= msgp
            response["prefix"] = "gt_tareas"
            response["title"] = "Alertas del Momento Anotar"
            response["serverAction"] = "opciones_recordatorio_anotar"
            response["customButtons"] = botones
            
            response['params'] = [
                
            ]
        
            return response

        response["resul"] = True
        response["msg"] = "No tienes alertas en el momento anotar"
        return response

    def gesttare_opciones_recordatorio_planear(self, oParam):
        user_name = qsatype.FLUtil.nameUser()
        valores = flgesttare_def.iface.revisar_indicadores(user_name)
        # msgp = []
        msg = []
        botones = []
        clase = []
        titulo_acordeon = []
        response = {}
        if 'tarea_sin' in valores and valores['tarea_sin']:
            clase.append("revisada_anotar")
            # msg.append("<strong>CONSEJO: </strong>Tienes tareas en sin fecha de ejecución que llevan más de 30 días sin movimiento. Te aconsejamos que las revises para poder incluirlas en tu próxima planeación semanal, o bien para deshacer el compromiso.")
            # msgp.append("¿Quieres revisar la bandeja de entrada?")
            msg.append("<img src='/static/dist/img/icons/diagrama-tareas-sin-planear.svg' style='width:600px; height:300px; margin-top:-30px; margin-left:auto; margin-right:auto; display:block; margin-bottom:-60px;'></img><br/> <a href='http://doc.dailyjob.io/books/manual-de-usuario/chapter/momento-planear' class='btn btn-primary btn-submit modal-btn' target='_blank'>Aprender más</a>")
            if valores["tarea_sin"] > 1:
                nombre = "Tienes {} tareas sin planificar".format(valores['tarea_sin'])
            else:
                nombre = "Tienes {} tarea sin planificar".format(valores['tarea_sin'])
            titulo_acordeon.append(nombre)
            botones.append({"accion": "goto","nombre": "Revisar tareas", "url": "/gesttare/gt_tareas/custom/recordatorioPlanear"})

            response['status'] = 4
            response['data'] = {}
            response["clase"] = clase
            response["titulo_acordeon"] = titulo_acordeon
            response["msg"]= msg
            # response["msgp"]= msgp
            response["prefix"] = "gt_tareas"
            response["title"] = "Alertas del Momento Planear"
            response["serverAction"] = "opciones_recordatorio_anotar"
            response["customButtons"] = botones
            
            response['params'] = [
            ]
            
            return response

        response["resul"] = True
        response["msg"] = "No tienes alertas en el momento planear"
        return response

    def gesttare_opciones_recordatorio_analizar(self, oParam):
        
        response = {}

        response["resul"] = True
        response["msg"] = "No tienes alertas en el momento analizar"
        return response

    def __init__(self, context=None):
        super().__init__(context)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def getParticipantesProyecto(self, model, oParam):
        return self.ctx.gesttare_getParticipantesProyecto(model, oParam)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def iniciaValoresLabel(self, model, template=None, cursor=None, data=None):
        return self.ctx.gesttare_iniciaValoresLabel(model, template, cursor, data)

    def seconds_to_time(self, seconds, total=False, all_in_hours=False):
        return self.ctx.gesttare_seconds_to_time(seconds, total, all_in_hours)

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

    def field_completaIcon(self, model):
        return self.ctx.gesttare_field_completaIcon(model)

    def field_trackingIcon(self, model):
        return self.ctx.gesttare_field_trackingIcon(model)

    def field_completaTitle(self, model):
        return self.ctx.gesttare_field_completaTitle(model)

    def ren_field_proyecto(self, model):
        return self.ctx.gesttare_ren_field_proyecto(model)

    def ren_field_proyecto_espera(self, model):
        return self.ctx.gesttare_ren_field_proyecto_espera(model)

    def field_usuario(self, model):
        return self.ctx.gesttare_field_usuario(model)

    def color_fecha(self, model):
        return self.ctx.gesttare_color_fecha(model)

    def color_fechaentrega(self, model):
        return self.ctx.gesttare_color_fechaentrega(model)

    def ren_color_fecha(self, model):
        return self.ctx.gesttare_ren_color_fecha(model)

    def ren_color_fechaentrega(self, model):
        return self.ctx.gesttare_ren_color_fechaentrega(model)

    def ren_color_fecha_espera(self, model):
        return self.ctx.gesttare_ren_color_fecha_espera(model)

    def ren_color_fechaentrega_espera(self, model):
        return self.ctx.gesttare_ren_color_fechaentrega_espera(model)

    def color_nombre(self, model):
        return self.ctx.gesttare_color_nombre(model)

    def color_nombreProyecto(self, model):
        return self.ctx.gesttare_color_nombreProyecto(model)

    def color_fondo_estado(self, model):
        return self.ctx.gesttare_color_fondo_estado(model)

    def color_fondo_estado_revision(self, model):
        return self.ctx.gesttare_color_fondo_estado_revision(model)

    def color_responsable(self, model):
        return self.ctx.gesttare_color_responsable(model)

    def uploadFile(self, model, oParam):
        return self.ctx.gesttare_uploadFile(model, oParam)

    def uploadFileTarea(self, model, oParam):
        return self.ctx.gesttare_uploadFileTarea(model, oParam)

    def login(self, oParam):
        return self.ctx.gesttare_login(oParam)

    def getpryus(self, appid, email):
        return self.ctx.gesttare_getpryus(appid, email)

    def damepryus(self, appid, email):
        return self.ctx.gesttare_damepryus(appid, email)

    def dameProyectos(self, idusuario):
        return self.ctx.gesttare_dameProyectos(idusuario)

    def dameHitos(self, idproyecto):
        return self.ctx.gesttare_dameHitos(idproyecto)

    def dameUsuarios(self, idusuario):
        return self.ctx.gesttare_dameUsuarios(idusuario)

    def startstop(self, model, oParam, cursor):
        return self.ctx.gesttare_startstop(model, oParam, cursor)

    def completar_tarea(self, model, cursor):
        return self.ctx.gesttare_completar_tarea(model, cursor)

    def abrir_tarea(self, model, cursor):
        return self.ctx.gesttare_abrir_tarea(model, cursor)

    def incrementar_dia(self, model, cursor):
        return self.ctx.gesttare_incrementar_dia(model, cursor)

    def ejecucion_hoy(self, model, cursor):
        return self.ctx.gesttare_ejecucion_hoy(model, cursor)

    def un_dia(self, model, cursor):
        return self.ctx.gesttare_un_dia(model, cursor)

    def semana_siguiente(self, model, cursor):
        return self.ctx.gesttare_semana_siguiente(model, cursor)

    def elegir_fecha(self, model, cursor):
        return self.ctx.gesttare_elegir_fecha(model, cursor)

    def fecha_elegida(self, model, oParam, cursor):
        return self.ctx.gesttare_fecha_elegida(model, oParam, cursor)

    def quitar_fecha_modal(self, model, cursor):
        return self.ctx.gesttare_quitar_fecha_modal(model, cursor)

    def quitar_fecha_espera(self, model, cursor):
        return self.ctx.gesttare_quitar_fecha_espera(model, cursor)

    def quitar_fecha_hacer(self, model, cursor):
        return self.ctx.gesttare_quitar_fecha_hacer(model, cursor)

    def calcula_totaltiempo(self, cursor):
        return self.ctx.gesttare_calcula_totaltiempo(cursor)

    def creartarea(self, oParam):
        return self.ctx.gesttare_creartarea(oParam)

    def createtask(self, oParam):
        return self.ctx.gesttare_createtask(oParam)

    def createinbox(self, oParam):
        return self.ctx.gesttare_createinbox(oParam)

    def actNuevoPartic(self, oParam, cursor):
        return self.ctx.gesttare_actNuevoPartic(oParam, cursor)

    def bChCursor(self, fN, cursor):
        return self.ctx.gesttare_bChCursor(fN, cursor)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def getTareasUsuario(self, oParam):
        return self.ctx.gesttare_getTareasUsuario(oParam)

    def check_permissions(self, model, prefix, pk, template, acl, accion=None):
        return self.ctx.gesttare_check_permissions(model, prefix, pk, template, acl, accion)

    def borrar_tarea(self, model, oParam, cursor):
        return self.ctx.gesttare_borrar_tarea(model, oParam, cursor)

    def gotoGestionarTiempo(self, model, cursor):
        return self.ctx.gesttare_gotoGestionarTiempo(model, cursor)

    def commonCalculateField(self, fN, cursor):
        return self.ctx.gesttare_commonCalculateField(fN, cursor)

    def verTrackingTarea(self, cursor):
        return self.ctx.gesttare_verTrackingTarea(cursor)

    def gotoTarea(self, model):
        return self.ctx.gesttare_gotoTarea(model)

    def gotoReturnActualizacion(self, oParam):
        return self.ctx.gesttare_gotoReturnActualizacion(oParam)

    def queryGrid_renegociacion(self, model):
        return self.ctx.gesttare_queryGrid_renegociacion(model)

    def queryGrid_revisionTareas(self, model):
        return self.ctx.gesttare_queryGrid_revisionTareas(model)

    def queryGrid_revisionTareasTreinta(self, model):
        return self.ctx.gesttare_queryGrid_revisionTareasTreinta(model)

    def gotoNewRecordAnotacion(self, oParam):
        return self.ctx.gesttare_gotoNewRecordAnotacion(oParam)

    def gotoNewRecordRecordatorioAtrasada(self, oParam):
        return self.ctx.gesttare_gotoNewRecordRecordatorioAtrasada(oParam)

    def gotoNewRecordRecordatorioBandeja(self, oParam):
        return self.ctx.gesttare_gotoNewRecordRecordatorioBandeja(oParam)

    def gotoNewRecordRecordatorioEspera(self, oParam):
        return self.ctx.gesttare_gotoNewRecordRecordatorioEspera(oParam)

    def gotonewrecordtarea(self, oParam):
        return self.ctx.gesttare_gotonewrecordtarea(oParam)

    def drawif_completartarea(self, cursor):
        return self.ctx.gesttare_drawif_completartarea(cursor)

    def drawif_checkAdjuntos(self, cursor):
        return self.ctx.gesttare_drawif_checkAdjuntos(cursor)

    def drawif_checkActu2(self, cursor):
        return self.ctx.gesttare_drawif_checkActu2(cursor)

    def drawif_checkNormal(self, cursor):
        return self.ctx.gesttare_drawif_checkNormal(cursor)

    def drawif_abrirtarea(self, cursor):
        return self.ctx.gesttare_drawif_abrirtarea(cursor)

    def drawif_iniciartarea(self, cursor):
        return self.ctx.gesttare_drawif_iniciartarea(cursor)

    def drawif_parartarea(self, cursor):
        return self.ctx.gesttare_drawif_parartarea(cursor)

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.gesttare_iniciaValoresCursor(cursor)

    def verTarea(self, model, cursor):
        return self.ctx.gesttare_verTarea(model, cursor)

    def field_adjunto(self, model):
        return self.ctx.gesttare_field_adjunto(model)

    def validateCursor(self, cursor):
        return self.ctx.gesttare_validateCursor(cursor)

    def gotomomentos(self):
        return self.ctx.gesttare_gotomomentos()

    def opciones_recordatorio(self, oParam):
        return self.ctx.gesttare_opciones_recordatorio(oParam)

    def opciones_recordatorio_anotar(self, oParam):
        return self.ctx.gesttare_opciones_recordatorio_anotar(oParam)

    def opciones_recordatorio_planear(self, oParam):
        return self.ctx.gesttare_opciones_recordatorio_planear(oParam)

    def opciones_recordatorio_analizar(self, oParam):
        return self.ctx.gesttare_opciones_recordatorio_analizar(oParam)

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
