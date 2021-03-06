# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
from datetime import datetime
from YBUTILS.viewREST import cacheController
from models.flgesttare import flgesttare_def


class gesttare(interna):

    def gesttare_getDesc(self):
        return None

    def gesttare_get_model_info(self, model, data, ident, template, where_filter, qr):
        if template == "mastertimetracking":
            ntareas = ident["PAG"]["COUNT"] or 0
            if not where_filter:
                where_filter = "1 = 1"
                usuario = qsatype.FLUtil.nameUser()
                curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
                curProyectos.select("idusuario = '" + str(usuario) + "'")
                proin = "("
                while curProyectos.next():
                    curProyectos.setModeAccess(curProyectos.Browse)
                    curProyectos.refreshBuffer()
                    # proin.append(curProyectos.valueBuffer("idproyecto"))
                    proin = proin + "'" + str(curProyectos.valueBuffer("idproyecto")) + "', "
                proin = proin + " null)"
                where_filter += " AND (gt_proyectos.idproyecto IN " + proin + " OR gt_tareas.idproyecto IS NULL)"
                # if qr["qr_td[tarea]"]:
                #     where_filter += " AND gt_tareas.nombre LIKE '%" + qr["qr_td[tarea]"] + "%'"
                # if hasattr(qr, 'QueryDict'):
                #     where_filter += " AND gt_tareas.nombre LIKE '%" + qr["qr_td[tarea]"] + "%'"
                try:
                    where_filter += " AND gt_tareas.nombre LIKE '%" + qr["qr_td[tarea]"] + "%'"
                except Exception as e:
                    print(e)

            else:
                where_filter = "1 = 1 AND " + where_filter
                usuario = qsatype.FLUtil.nameUser()
                curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
                curProyectos.select("idusuario = '" + str(usuario) + "'")
                proin = "("
                while curProyectos.next():
                    curProyectos.setModeAccess(curProyectos.Browse)
                    curProyectos.refreshBuffer()
                    # proin.append(curProyectos.valueBuffer("idproyecto"))
                    proin = proin + "'" + str(curProyectos.valueBuffer("idproyecto")) + "', "
                proin = proin + " null)"
                where_filter += " AND (gt_proyectos.idproyecto IN " + proin + " OR gt_tareas.idproyecto IS NULL)"
                if qr["qr_td[tarea]"]:
                    where_filter += " AND gt_tareas.nombre LIKE '%" + qr["qr_td[tarea]"] + "%'"

            tiempototal = qsatype.FLUtil.quickSqlSelect("gt_timetracking INNER JOIN gt_tareas ON gt_timetracking.idtarea = gt_tareas.idtarea INNER JOIN gt_hitosproyecto ON gt_tareas.idhito = gt_hitosproyecto.idhito INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto INNER JOIN aqn_user ON gt_timetracking.idusuario = aqn_user.idusuario INNER JOIN gt_clientes ON gt_proyectos.idcliente = gt_clientes.idcliente", "SUM(totaltiempo)", where_filter) or 0
            ntareas = qsatype.FLUtil.quickSqlSelect("gt_timetracking INNER JOIN gt_tareas ON gt_timetracking.idtarea = gt_tareas.idtarea INNER JOIN gt_hitosproyecto ON gt_tareas.idhito = gt_hitosproyecto.idhito INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto INNER JOIN aqn_user ON gt_timetracking.idusuario = aqn_user.idusuario INNER JOIN gt_clientes ON gt_proyectos.idcliente = gt_clientes.idcliente", "COUNT(DISTINCT(gt_tareas.idtarea))", where_filter) or 0

            tiempototal = flgesttare_def.iface.seconds_to_time(tiempototal.total_seconds(), all_in_hours=True)
            return {"masterTimeTracking": "Tiempo total: {} - Nº DE TAREAS: {}".format(tiempototal, ntareas)}

        elif template == "mastertimetrackingagrupado":
            ntareas = ident["PAG"]["COUNT"] or 0
            if not where_filter:
                where_filter = "1 = 1"
                usuario = qsatype.FLUtil.nameUser()
                curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
                curProyectos.select("idusuario = '" + str(usuario) + "'")
                proin = "("
                while curProyectos.next():
                    curProyectos.setModeAccess(curProyectos.Browse)
                    curProyectos.refreshBuffer()
                    # proin.append(curProyectos.valueBuffer("idproyecto"))
                    proin = proin + "'" + str(curProyectos.valueBuffer("idproyecto")) + "', "
                proin = proin + " null)"
                where_filter += " AND (gt_proyectos.idproyecto IN " + proin + " OR gt_tareas.idproyecto IS NULL)"
                try:
                    where_filter += " AND gt_tareas.nombre LIKE '%" + qr["qr_td[tarea]"] + "%'"
                except Exception as e:
                    print(e)
            else:
                where_filter = "1 = 1 AND " + where_filter
                usuario = qsatype.FLUtil.nameUser()
                curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
                curProyectos.select("idusuario = '" + str(usuario) + "'")
                proin = "("
                while curProyectos.next():
                    curProyectos.setModeAccess(curProyectos.Browse)
                    curProyectos.refreshBuffer()
                    # proin.append(curProyectos.valueBuffer("idproyecto"))
                    proin = proin + "'" + str(curProyectos.valueBuffer("idproyecto")) + "', "
                proin = proin + " null)"
                where_filter += " AND (gt_proyectos.idproyecto IN " + proin + " OR gt_tareas.idproyecto IS NULL)"
                if qr["qr_td[tarea]"]:
                    where_filter += " AND gt_tareas.nombre LIKE '%" + qr["qr_td[tarea]"] + "%'"

            tiempototal = qsatype.FLUtil.quickSqlSelect("gt_timetracking INNER JOIN gt_tareas ON gt_timetracking.idtarea = gt_tareas.idtarea INNER JOIN gt_hitosproyecto ON gt_tareas.idhito = gt_hitosproyecto.idhito INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto INNER JOIN aqn_user ON gt_timetracking.idusuario = aqn_user.idusuario INNER JOIN gt_clientes ON gt_proyectos.idcliente = gt_clientes.idcliente", "SUM(totaltiempo)", where_filter) or 0
            ntareas = qsatype.FLUtil.quickSqlSelect("gt_timetracking INNER JOIN gt_tareas ON gt_timetracking.idtarea = gt_tareas.idtarea INNER JOIN gt_hitosproyecto ON gt_tareas.idhito = gt_hitosproyecto.idhito INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto INNER JOIN aqn_user ON gt_timetracking.idusuario = aqn_user.idusuario INNER JOIN gt_clientes ON gt_proyectos.idcliente = gt_clientes.idcliente", "COUNT(DISTINCT(gt_tareas.idtarea))", where_filter) or 0

            tiempototal = flgesttare_def.iface.seconds_to_time(tiempototal.total_seconds(), all_in_hours=True)
            return {"masterTimeTrackingAgrupado": "Tiempo total: {} - Nº DE TAREAS: {}".format(tiempototal, ntareas)}
        return None

    def gesttare_queryGrid_mastertimetracking(self, model, filters):
        where = "1 = 1"
        usuario = qsatype.FLUtil.nameUser()
        curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
        curProyectos.select("idusuario = '" + str(usuario) + "'")
        proin = "("

        while curProyectos.next():
            curProyectos.setModeAccess(curProyectos.Browse)
            curProyectos.refreshBuffer()
            # proin.append(curProyectos.valueBuffer("idproyecto"))
            if curProyectos.valueBuffer("idproyecto") and curProyectos.valueBuffer("tipo") != "observador":
                proin = proin + "'" + str(curProyectos.valueBuffer("idproyecto")) + "', "

        proin = proin + " null)"
        where += " AND (gt_proyectos.idproyecto IN " + proin + " OR gt_tareas.idproyecto IS NULL)"

        if filters:
            if "[proyecto]" in filters and filters["[proyecto]"] != "":
                where += " AND gt_proyectos.idproyecto = '{}'".format(filters["[proyecto]"])
            if "[tarea]" in filters and filters["[tarea]"] != "":
                where += " AND UPPER(gt_tareas.nombre) like '%{}%'".format(filters["[tarea]"].upper())
            if "[usuario]" in filters and filters["[usuario]"] != "":
                where += " AND aqn_user.idusuario = '{}'".format(filters["[usuario]"])
            if "[d_fecha]" in filters and filters["[d_fecha]"] != "":
                where += " AND gt_timetracking.fecha >= '{}'".format(filters["[d_fecha]"])
            if "[h_fecha]" in filters and filters["[h_fecha]"] != "":
                where += " AND gt_timetracking.fecha <= '{}'".format(filters["[h_fecha]"])
            if "[fecha]" in filters and filters["[fecha]"] != "":
                where += " AND gt_timetracking.fecha = '{}'".format(filters["[fecha]"])
            if "[hito]" in filters and filters["[hito]"] != "":
                where += " AND gt_hitosproyecto.idhito = '{}'".format(filters["[hito]"])
            if "[cliente]" in filters and filters["[cliente]"] != "":
                where += " AND gt_proyectos.idcliente = '{}'".format(filters["[cliente]"])
            if "[buscador]" in filters and filters["[buscador]"] != "":
                where += " AND UPPER(gt_proyectos.nombre) LIKE '%" + filters["[buscador]"].upper() + "%' OR UPPER(gt_tareas.nombre) LIKE '%" + filters["[buscador]"].upper() + "%' OR UPPER(aqn_user.nombre) LIKE '%" + filters["[buscador]"].upper() + "%'"

        query = {}
        query["tablesList"] = ("gt_timetracking, gt_tareas, aqn_user, gt_hitosproyecto")
        query["select"] = ("gt_timetracking.idtracking, gt_hitosproyecto.nombre, gt_timetracking.fecha, gt_timetracking.horainicio, gt_timetracking.horafin, gt_timetracking.totaltiempo, gt_tareas.nombre, gt_proyectos.nombre, aqn_user.usuario, gt_proyectos.idcliente, aqn_user.nombre")
        query["from"] = ("gt_timetracking INNER JOIN gt_tareas ON gt_timetracking.idtarea = gt_tareas.idtarea LEFT OUTER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto INNER JOIN aqn_user ON gt_timetracking.idusuario = aqn_user.idusuario INNER JOIN gt_hitosproyecto ON gt_hitosproyecto.idhito = gt_tareas.idhito")
        query["where"] = (where)
        query["orderby"] = ("gt_timetracking.fecha DESC, gt_timetracking.horainicio DESC")
        return query

    def gesttare_queryGrid_mastertimetrackingagrupado(self, model, filters):
        where = "1 = 1"
        usuario = qsatype.FLUtil.nameUser()
        curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
        curProyectos.select("idusuario = '" + str(usuario) + "'")
        proin = "("

        while curProyectos.next():
            curProyectos.setModeAccess(curProyectos.Browse)
            curProyectos.refreshBuffer()
            # proin.append(curProyectos.valueBuffer("idproyecto"))
            if curProyectos.valueBuffer("idproyecto") and curProyectos.valueBuffer("tipo") != "observador":
                proin = proin + "'" + str(curProyectos.valueBuffer("idproyecto")) + "', "

        proin = proin + " null)"
        where += " AND (gt_proyectos.idproyecto IN " + proin + " OR gt_tareas.idproyecto IS NULL)"

        if filters:
            if "[proyecto]" in filters and filters["[proyecto]"] != "":
                where += " AND gt_proyectos.idproyecto = '{}'".format(filters["[proyecto]"])
            if "[tarea]" in filters and filters["[tarea]"] != "":
                where += " AND UPPER(gt_tareas.nombre) like '%{}%'".format(filters["[tarea]"].upper())
            if "[usuario]" in filters and filters["[usuario]"] != "":
                where += " AND aqn_user.idusuario = '{}'".format(filters["[usuario]"])
            if "[d_fecha]" in filters and filters["[d_fecha]"] != "":
                where += " AND gt_timetracking.fecha >= '{}'".format(filters["[d_fecha]"])
            if "[h_fecha]" in filters and filters["[h_fecha]"] != "":
                where += " AND gt_timetracking.fecha <= '{}'".format(filters["[h_fecha]"])
            if "[fecha]" in filters and filters["[fecha]"] != "":
                where += " AND gt_timetracking.fecha = '{}'".format(filters["[fecha]"])
            if "[hito]" in filters and filters["[hito]"] != "":
                where += " AND gt_hitosproyecto.idhito = '{}'".format(filters["[hito]"])
            if "[buscador]" in filters and filters["[buscador]"] != "":
                where += " AND UPPER(gt_proyectos.nombre) LIKE '%" + filters["[buscador]"].upper() + "%' OR UPPER(gt_tareas.nombre) LIKE '%" + filters["[buscador]"].upper() + "%' OR UPPER(aqn_user.nombre) LIKE '%" + filters["[buscador]"].upper() + "%'"

        query = {}
        query["tablesList"] = ("gt_timetracking, gt_tareas, gt_proyectos")
        query["select"] = ("gt_tareas.idtarea, gt_tareas.nombre, gt_proyectos.nombre,SUM(gt_timetracking.totaltiempo)")
        query["from"] = ("gt_timetracking INNER JOIN gt_tareas ON gt_timetracking.idtarea = gt_tareas.idtarea LEFT OUTER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto INNER JOIN aqn_user ON gt_timetracking.idusuario = aqn_user.idusuario")
        query["where"] = (where)
        query["groupby"] = "gt_timetracking.idtarea, gt_tareas.idtarea, gt_proyectos.idproyecto"
        query["orderby"] = ("SUM(gt_timetracking.totaltiempo) DESC")
        return query

    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        if template == "mastertimetracking":
            # return [{'verbose_name': 'nombreusuario', 'func': 'field_nombre'}]
            fields = [
                {'verbose_name': 'Color usuario', 'func': 'color_usuario'},
                {'verbose_name': 'aqn_user.usuario', 'func': 'field_nombre'},
                {'verbose_name': 'Proyecto', 'func': 'field_proyecto'},
                {'verbose_name': 'Color nombre proyecto', 'func': 'color_nombreProyectoT'},
                {'verbose_name': 'Cliente', 'func': 'field_cliente'}
            ]
        elif template == "mastertimetrackingagrupado":
            fields = [
                {'verbose_name': 'Proyecto', 'func': 'field_proyecto'},
                {'verbose_name': 'Color nombre proyecto', 'func': 'color_nombreProyecto'},
                {'verbose_name': 'suma', 'func': 'field_sumTotalTiempo'}

            ]
        return fields

    def gesttare_field_nombre(self, model):
        nombre = ""
        try:
            nombre = "@" + model['aqn_user.usuario']
            # if hasattr(model.idusuario, 'usuario'):
            #     nombre = "@" + model.idusuario.usuario
            #     print("el nombre es: ",nombre)
        except Exception as e:
            print(e)
        return nombre

    def gesttare_color_nombreProyecto(self, model):
        username = qsatype.FLUtil.nameUser()
        id_compania_usuario = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(username))
        color = ""
        try:
            id_proyecto = qsatype.FLUtil.quickSqlSelect("gt_tareas", "idproyecto", "idtarea = {}".format(str(model["gt_tareas.idtarea"])))
            # if idproyecto:
            tipo_participante = qsatype.FLUtil.quickSqlSelect("gt_particproyecto", "tipo", "idusuario = '{}' AND idproyecto = {}".format(username, str(id_proyecto)))
            id_compania_proyecto = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "idcompany", "idproyecto = '{}'".format(id_proyecto))
            if tipo_participante == "observador":
                color = "OBSER "
            if id_compania_proyecto != id_compania_usuario and tipo_participante != "observador":
                color = "COL "
            if id_compania_proyecto == id_compania_usuario:
                color = "INTERNO_EMPRESA "
        except:
            pass
        return color

    def gesttare_color_nombreProyectoT(self, model):
        username = qsatype.FLUtil.nameUser()
        id_compania_usuario = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(username))
        color = ""
        try:
            id_tarea = qsatype.FLUtil.quickSqlSelect("gt_timetracking", "idtarea", "idtracking = {}".format(str(model["pk"])))
            id_proyecto = qsatype.FLUtil.quickSqlSelect("gt_tareas", "idproyecto", "idtarea = {}".format(str(id_tarea)))
            # if idproyecto:
            tipo_participante = qsatype.FLUtil.quickSqlSelect("gt_particproyecto", "tipo", "idusuario = '{}' AND idproyecto = {}".format(username, str(id_proyecto)))
            id_compania_proyecto = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "idcompany", "idproyecto = '{}'".format(id_proyecto))
            if tipo_participante == "observador":
                color = "OBSER "
            if id_compania_proyecto != id_compania_usuario and tipo_participante != "observador":
                color = "COL "
            if id_compania_proyecto == id_compania_usuario:
                color = "INTERNO_EMPRESA "
        except:
            pass
        return color

    def gesttare_seconds_to_time(self, seconds, total=False, all_in_hours=False):
        if not seconds:
            if total:
                seconds = 0
            else:
                return ""

        minutes = seconds // 60
        seconds = int(seconds % 60)
        hours = int(minutes // 60)
        minutes = int(minutes % 60)

        days = None
        years = None

        if not all_in_hours:
            days = hours // 24
            hours = int(hours % 24)
            years = days // 365
            days = int(days % 365)

        seconds = str(seconds) if seconds >= 10 else "0{}".format(seconds)
        minutes = str(minutes) if minutes >= 10 else "0{}".format(minutes)
        hours = str(hours) if hours >= 10 else "0{}".format(hours)

        if total:
            years = "" if not years else "{} años, ".format(years)
            days = "" if not days else "{} días, ".format(days)
            return "{}{}{}:{}:{}".format(years, days, hours, minutes, seconds)
        else:
            return "{}:{}:{}".format(hours, minutes, seconds)

    def gesttare_time_to_seconds(self, time):
        seconds = 0
        a_time = time.split(":")

        if len(a_time) > 0:
            seconds = seconds + int(a_time[0]) * 3600
        if len(a_time) > 1:
            seconds = seconds + int(a_time[1]) * 60
        if len(a_time) > 2:
            seconds = seconds + int(a_time[2])

        return seconds

    def gesttare_calcula_totaltiempo(self, cursor):
        formato = "%H:%M:%S"
        horainicio = str(cursor.valueBuffer("horainicio"))
        if len(horainicio) == 5:
            horainicio += ":00"
        horafin = str(cursor.valueBuffer("horafin"))
        if len(horafin) == 5:
            horafin += ":00"
        hfin = datetime.strptime(horafin, formato)
        hinicio = datetime.strptime(horainicio, formato)
        totaltiempo = hfin - hinicio
        totaltiempo = str(totaltiempo)
        if len(totaltiempo) < 8:
            totaltiempo = "0" + totaltiempo
        if len(totaltiempo) > 8:
            totaltiempo = totaltiempo[8:]
        return totaltiempo

    def gesttare_editarTT(self, oParam, cursor):
        response = {}

        if "tiempototal" not in oParam:
            response["status"] = -1
            response["data"] = {}
            response["params"] = [
                {
                    "componente": "YBFieldDB",
                    "prefix": "gt_timetracking",
                    "style": {
                        "width": "100%"
                    },
                    "value": self.seconds_to_time(cursor.valueBuffer("totaltiempo")),
                    "tipo": 27,
                    "verbose_name": "Tiempo total",
                    "label": "Tiempo total",
                    "key": "tiempototal",
                    "validaciones": None,
                    "required": False
                }
            ]
            return response
        else:
            seconds = self.time_to_seconds(oParam["tiempototal"])
            nuevo_fin = cursor.valueBuffer("horainicio") + seconds

            cursor.setValueBuffer("horafin", nuevo_fin)
            cursor.setValueBuffer("totaltiempo", seconds)

            if not cursor.commitBuffer():
                print("Ocurrió un error al actualizar el registro de timetracking")
                return False
            return True

    def gesttare_iniciaValoresCursor(self, cursor=None):
        usuario = qsatype.FLUtil.nameUser()
        cursor.setValueBuffer(u"idusuario", usuario)

        qsatype.FactoriaModulos.get('formRecordgt_timetracking').iface.iniciaValoresCursor(cursor)
        return True

    def gesttare_bChCursor(self, fN, cursor):
        # if not qsatype.FactoriaModulos.get('formRecordgt_timetracking').iface.bChCursor(fN, cursor):
        #     return False
        if fN == "horainicio" or fN == "horafin":
            totaltiempo = self.calcula_totaltiempo(cursor)
            cursor.setValueBuffer("totaltiempo", totaltiempo)

        if fN == u"costehora" or fN == u"totaltiempo":
            cursor.setValueBuffer(u"coste", flgesttare_def.iface.calcula_costetiempo("timetracking", cursor))

        return True

    def gesttare_check_permissions(self, model, prefix, pk, template, acl, accion):
        if template == "accion":
            if accion == "delete":
                curTracking = qsatype.FLSqlCursor("gt_timetracking")
                curTracking.select(ustr("idtracking = '", pk, "'"))
                curTracking.refreshBuffer()
                if curTracking.first():
                    curTracking.setModeAccess(curTracking.Browse)
                    curTracking.refreshBuffer()
                    idusuario = curTracking.valueBuffer("idusuario")
                    usuario = qsatype.FLUtil.nameUser()
                    if not str(idusuario) == usuario:
                        return False

        # if template == "formRecord":
        #     curTracking = qsatype.FLSqlCursor("gt_timetracking")
        #     curTracking.select(ustr("idtracking = '", pk, "'"))
        #     curTracking.refreshBuffer()
        #     if curTracking.first():
        #         usuario = qsatype.FLUtil.nameUser()
        #         curTracking.setModeAccess(curTracking.Browse)
        #         curTracking.refreshBuffer()
        #         # idtarea = curTracking.valueBuffer("idtarea")
        #         # idproyecto = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"idproyecto", ustr(u"idtarea = '", idtarea, u"'"))
        #         # nombreUsuario = qsatype.FLUtil.nameUser()
        #         # pertenece = qsatype.FLUtil.sqlSelect(u"gt_particproyecto", u"idusuario", ustr(u"idusuario = '", nombreUsuario, u"' AND idproyecto = '", idproyecto, "'"))
        #         pertenece = str(curTracking.valueBuffer("idusuario")) == str(usuario)
        #         print(usuario)
        #         print(curTracking.valueBuffer("idusuario"))
        #         if not pertenece:
        #             return False
        #     else:
        #         return False
        return True

    def gesttare_verTarea(self, model, cursor):
        url = "/gesttare/gt_tareas/" + str(cursor.valueBuffer("idtarea"))
        return url

    def gesttare_color_usuario(self, model):
        # print(model['aqn_user.usuario'])
        # if (model['aqn_user.usuario']):
        #     return "usuario"

        return "usuario"

    def gesttare_checkTimeTrackingDraw(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        # is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        pertenece = str(cursor.valueBuffer("idusuario")) == str(usuario)
        if not pertenece:
            return "disabled"
        return True

    def gesttare_field_proyecto(self, model):
        # proyecto = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "nombre", "idproyecto = '{}'".format(model.idproyecto)) or ""
        nombreUsuario = qsatype.FLUtil.nameUser()
        id_compania_usuario = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(nombreUsuario))
        try:
            proyecto = model['gt_proyectos.nombre']
            idcliente = model['gt_proyectos.idcliente']
            if idcliente:
                codcliente = qsatype.FLUtil.sqlSelect(u"gt_clientes", u"codcliente", ustr(u"idcliente = '", str(idcliente), u"'"))
                id_tarea = qsatype.FLUtil.quickSqlSelect("gt_timetracking", "idtarea", "idtracking = {}".format(str(model["pk"])))
                id_proyecto = qsatype.FLUtil.quickSqlSelect("gt_tareas", "idproyecto", "idtarea = {}".format(str(id_tarea)))
                # print("id_proyecto", id_proyecto)
                id_compania_proyecto = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "idcompany", "idproyecto = {}".format(str(id_proyecto)))
                # codcliente = model.idproyecto.idcliente.codcliente
                if codcliente and id_compania_proyecto == id_compania_usuario:
                    proyecto = "#" + codcliente + " " + proyecto
        except:
            pass
        return proyecto

    def gesttare_field_cliente(self, model):
        cliente = ""
        idcliente = model['gt_proyectos.idcliente']
        if idcliente:
            cliente = qsatype.FLUtil.sqlSelect(u"gt_clientes", u"nombre", ustr(u"idcliente = '", str(idcliente), u"'"))
        return cliente

    def gesttare_field_sumTotalTiempo(self, model):
        # proyecto = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "nombre", "idproyecto = '{}'".format(model.idproyecto)) or ""
        suma = model['SUM(gt_timetracking.totaltiempo)']
        tiempototal = flgesttare_def.iface.seconds_to_time(suma.total_seconds(), all_in_hours=True)

        return tiempototal

    def gesttare_get_estado(self):
        estado = cacheController.getSessionVariable("estado_timetracking", None)

        if not estado:
            self.iface.set_estado("noagrupado")
            estado = "noagrupado"

        return estado

    def gesttare_set_estado(self, estado):
        cacheController.setSessionVariable("estado_timetracking", estado)
        response = {}
        response["msg"] = ""
        return response

    def gesttare_drawif_noagrupado(self, cursor):
        if self.iface.get_estado() != "noagrupado":
            return "hidden"

    def gesttare_drawif_agrupado(self, cursor):
        if self.iface.get_estado() != "agrupado":
            return "hidden"

    def gesttare_drawif_botonnoagrupado(self, cursor):
        if self.iface.get_estado() == "noagrupado":
            return "hidden"

    def gesttare_drawif_botonagrupado(self, cursor):
        if self.iface.get_estado() == "agrupado":
            return "hidden"

    def __init__(self, context=None):
        super().__init__(context)

    def field_proyecto(self, model):
        return self.ctx.gesttare_field_proyecto(model)

    def field_sumTotalTiempo(self, model):
        return self.ctx.gesttare_field_sumTotalTiempo(model)

    def field_cliente(self, model):
        return self.ctx.gesttare_field_cliente(model)

    def checkTimeTrackingDraw(self, cursor):
        return self.ctx.gesttare_checkTimeTrackingDraw(cursor)

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.gesttare_iniciaValoresCursor(cursor)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def get_model_info(self, model, data, ident, template, where_filter, qr):
        return self.ctx.gesttare_get_model_info(model, data, ident, template, where_filter, qr)

    def queryGrid_mastertimetracking(self, model, filters):
        return self.ctx.gesttare_queryGrid_mastertimetracking(model, filters)

    def queryGrid_mastertimetrackingagrupado(self, model, filters):
        return self.ctx.gesttare_queryGrid_mastertimetrackingagrupado(model, filters)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def seconds_to_time(self, seconds, total=False, all_in_hours=False):
        return self.ctx.gesttare_seconds_to_time(seconds, total, all_in_hours)

    def time_to_seconds(self, time):
        return self.ctx.gesttare_time_to_seconds(time)

    def editarTT(self, oParam, cursor):
        return self.ctx.gesttare_editarTT(oParam, cursor)

    def bChCursor(self, fN, cursor):
        return self.ctx.gesttare_bChCursor(fN, cursor)

    def calcula_totaltiempo(self, cursor):
        return self.ctx.gesttare_calcula_totaltiempo(cursor)

    def check_permissions(self, model, prefix, pk, template, acl, accion=None):
        return self.ctx.gesttare_check_permissions(model, prefix, pk, template, acl, accion)

    def field_nombre(self, model):
        return self.ctx.gesttare_field_nombre(model)

    def verTarea(self, model, cursor):
        return self.ctx.gesttare_verTarea(model, cursor)

    def color_usuario(self, model):
        return self.ctx.gesttare_color_usuario(model)

    def get_estado(self):
        return self.ctx.gesttare_get_estado()

    def set_estado(self, estado):
        return self.ctx.gesttare_set_estado(estado)

    def drawif_noagrupado(self, cursor):
        return self.ctx.gesttare_drawif_noagrupado(cursor)

    def drawif_agrupado(self, cursor):
        return self.ctx.gesttare_drawif_agrupado(cursor)

    def drawif_botonnoagrupado(self, cursor):
        return self.ctx.gesttare_drawif_botonnoagrupado(cursor)

    def drawif_botonagrupado(self, cursor):
        return self.ctx.gesttare_drawif_botonagrupado(cursor)

    def color_nombreProyecto(self, model):
        return self.ctx.gesttare_color_nombreProyecto(model)

    def color_nombreProyectoT(self, model):
        return self.ctx.gesttare_color_nombreProyectoT(model)



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
