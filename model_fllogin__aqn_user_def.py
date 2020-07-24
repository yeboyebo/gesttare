
# @class_declaration gesttare #
from models.flgesttare import flgesttare_def
import datetime
from datetime import date
import calendar
import locale
from YBUTILS.APIQSA import APIQSA

class gesttare(yblogin):

    def gesttare_get_model_info(self, model, data, ident, template, where_filter):
        if template == "analisis":
            tengopermiso = flgesttare_def.iface.compruebaPermisosPlan("titulo_analisis")
            if tengopermiso != True:
                return tengopermiso
            return {"graficosAnalisis": "Informe individual"}
        return None

    def get_model_info(self, model, data, ident, template, where_filter):
        return self.ctx.gesttare_get_model_info(model, data, ident, template, where_filter)

    def gesttare_getUsuariosProyecto(self, oParam):
        data = []
        if "idproyecto" not in oParam or oParam['idproyecto'] == None:
            qsatype.FLUtil.ponMsgError("Debes seleccionar la persona responsable del listado de participantes de este proyecto para que la tarea se guarde correctamente")
            return data
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_proyectos, gt_particproyecto, aqn_user")
        q.setSelect(u"DISTINCT(p.idusuario), u.usuario")
        q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.idproyecto=p.idproyecto INNER JOIN aqn_user u ON u.idusuario =p.idusuario")
        q.setWhere(u"t.idproyecto = '" + str(oParam['idproyecto']) + "' AND (UPPER(u.usuario) LIKE UPPER('%" + oParam["val"] + "%') OR UPPER(u.email) LIKE UPPER('%" + oParam["val"] + "%')) AND u.activo AND (p.tipo <> 'observador' or p.tipo = 'colaborador' or p.tipo is null) ORDER BY u.usuario LIMIT 7")

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

    def gesttare_getParticipantesProyecto(self, oParam):
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_tareas, gt_particproyecto, aqn_user")
        q.setSelect(u"p.idusuario, u.usuario")
        q.setFrom(u"gt_tareas t LEFT JOIN gt_particproyecto p ON t.idproyecto=p.idproyecto INNER JOIN aqn_user u ON u.idusuario =p.idusuario")
        q.setWhere(u"t.idtarea = '" + str(oParam['pk']) + "' AND UPPER(u.usuario) LIKE UPPER('%" + oParam["val"] + "%')  ORDER BY u.usuario LIMIT 7")

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

    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        if template == "mastertimetracking":
            return [{'verbose_name': 'nombreusuario', 'func': 'field_nombre'}]
        if template == "formRecord":
            return [{'verbose_name': 'usuario', 'func': 'field_nombreform'}]
        if template == "master":
            return [{'verbose_name': 'completaIcon', 'func': 'field_completaIcon'}, {'verbose_name': 'completaTitle', 'func': 'field_completaTitle'}, {'verbose_name': 'Color usuario', 'func': 'color_usuario'}, {'verbose_name': 'usuario', 'func': 'field_nombre'}]
        # fields = [
            # {'verbose_name': 'Color usuario', 'func': 'color_usuario'},
            # {'verbose_name': 'usuario', 'func': 'field_nombre'}
        # ]
        return fields

    def gesttare_field_nombre(self, model):
        nombre = ""
        try:
            nombre = "@" + model.usuario
            # if hasattr(model.idusuario, 'usuario'):
            #     nombre = "@" + model.idusuario.usuario
            #     print("el nombre es: ",nombre)
        except Exception as e:
            print(e)
        return nombre

    def gesttare_field_nombreform(self, model):
        nombre = ""
        try:
            nombre = model.usuario
        except Exception as e:
            print(e)
        return nombre

    def gesttare_getParticProyectosUsu(self, oParam):
        usuario = qsatype.FLUtil.nameUser()
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_particproyecto, aqn_user")
        q.setSelect(u"DISTINCT(p.idusuario), u.usuario")
        q.setFrom(u"gt_particproyecto p INNER JOIN aqn_user u ON p.idusuario = u.idusuario")
        q.setWhere(u"p.idproyecto in (select p.idproyecto from gt_particproyecto p INNER JOIN aqn_user u  ON p.idusuario = u.idusuario where p.idusuario = '" + str(usuario) + "') AND UPPER(u.usuario) LIKE UPPER('%" + oParam["val"] + "%') AND u.activo  ORDER BY u.usuario LIMIT 7")
        # q.setWhere(u"t.idtarea = '" + str(oParam['pk']) + "' AND UPPER(u.nombre) LIKE UPPER('%" + oParam["val"] + "%')  ORDER BY u.nombre LIMIT 7")

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

    def gesttare_getUsuTutelados(self, oParam):
        usuario = qsatype.FLUtil.nameUser()
        is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        if is_superuser:
            return self.iface.getParticCompaniaUsu(oParam)
        else:
            data = []
            q = qsatype.FLSqlQuery()
            q.setTablesList(u"aqn_user")
            q.setSelect(u"DISTINCT(idusuario), usuario")
            q.setFrom(u"aqn_user")
            q.setWhere(u"(idusuario = '" + str(usuario) + "' OR idresponsable = '" + str(usuario) + "') AND UPPER(usuario) LIKE UPPER('%" + oParam["val"] + "%') AND activo  ORDER BY usuario LIMIT 7")

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

    def gesttare_getParticCompaniaUsu(self, oParam):
        usuario = qsatype.FLUtil.nameUser()
        idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"aqn_user")
        q.setSelect(u"idusuario, usuario")
        q.setFrom(u"aqn_user")
        q.setWhere(u"idcompany = '" + str(idcompany) + "' AND UPPER(usuario) LIKE UPPER('%" + oParam["val"] + "%') AND activo  ORDER BY usuario LIMIT 7")
        # q.setWhere(u"t.idtarea = '" + str(oParam['pk']) + "' AND UPPER(u.nombre) LIKE UPPER('%" + oParam["val"] + "%')  ORDER BY u.nombre LIMIT 7")

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

    def gesttare_getFilters(self, model, name, template=None):
        filters = []
        usuario = qsatype.FLUtil.nameUser()
        if name == 'usuariosCompania' and usuario != "admin":
            idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
            return [{'criterio': 'idcompany__exact', 'valor': idcompany}]
        return filters


    def gesttare_field_completaIcon(self, model):
        if model.activo:
            return "check_box"
        else:
            return "check_box_outline_blank"

        return ""

    def gesttare_field_completaTitle(self, model):
        if model.activo:
            return "Desactivar usuario"
        else:
            return "Activar usuario"

        return ""

    def gesttare_activar(self, model, oParam, cursor):
        response = {}
        if cursor.valueBuffer("activo"):
            if "confirmacion" in oParam and oParam["confirmacion"]:
                usuario = cursor.valueBuffer("idusuario")
                # datos_usuario = {
                #     "params": {
                #         "aqn_user": {
                #             "activo": False
                #         }
                #     }

                # }
                datos_usuario =  {
                    "pk": usuario,
                    "activo": False
                }
                APIQSA.entry_point('patch', "aqn_user", usuario, datos_usuario)

                # if not cursor_usuario:
                #     response["status"] = 1
                #     response["msg"] = "No se pudo desactivar usuario"
                #     return response
                if not qsatype.FLUtil.sqlDelete("gt_partictarea", "idusuario = " + str(usuario)):
                    response["status"] = 1
                    response["msg"] = "No se pudo desactivar usuario"
                    return response
                if not qsatype.FLUtil.sqlDelete("gt_particproyecto", "idusuario = " + str(usuario)):
                    response["status"] = 1
                    response["msg"] = "No se pudo desactivar usuario"
                    return response
                response["resul"] = True
                # response["msg"] = "Usuario " + cursor_usuario.valueBuffer("usuario") + " desactivado"
                response["msg"] = "Usuario " + cursor.valueBuffer("nombre") + " desactivado"

                return response

            response["status"] = 2
            response["confirm"] = "¿Seguro que quieres desactivar usuario?"
            return response

        if "confirmacion" in oParam and oParam["confirmacion"]:
                usuario = cursor.valueBuffer("idusuario")
                datos_usuario =  {
                    "pk": usuario,
                    "activo": True
                }
                APIQSA.entry_point('patch', "aqn_user", usuario, datos_usuario)
                # datos_usuario = {
                #     "params": {
                #         "aqn_user": {
                #             "activo": True
                #         }
                #     }
                # }
                # cursor_usuario = APIQSA.entry_point('post', "aqn_user", usuario, datos_usuario, "activar_usuario")
                # if not cursor_usuario:
                #     response["status"] = 1
                #     response["msg"] = "No se puede activar usuario"
                #     return response
                response["resul"] = True
                # response["msg"] = "Usuario " + cursor_usuario.valueBuffer("usuario") + " activado"
                response["msg"] = "Usuario " + cursor.valueBuffer("nombre") + " activado"
                return response

        response["status"] = 2
        response["confirm"] = "¿Seguro que quieres activar usuario?"
        return response

    def gesttare_checkCambiaPassword(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        if str(cursor.valueBuffer("idusuario")) == usuario:
            return True
        return "hidden"

    def gesttare_checkDrawUser(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        if not is_superuser:
            return "hidden"
        return True

    def gesttare_checkResponsableDraw(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        if not is_superuser:
            return "disabled"
        return True


    def gesttare_check_permissions(self, model, prefix, pk, template, acl, accion):
        usuario = qsatype.FLUtil.nameUser()
        isadmin = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        if template == "analisis":
            return True
        if pk == usuario:
            return True
        elif not isadmin and accion is None:
            return False
        return True

    def gesttare_graficoproyectosportiempo(self, oParam):
        tengopermiso = flgesttare_def.iface.compruebaPermisosPlan("informes_horizontal")
        if tengopermiso != True:
            return tengopermiso

        where = "1=1 "
        usuario = qsatype.FLUtil.nameUser()
        if not oParam:
            hoy = date.today()
            ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
            #where += " AND tt.fecha BETWEEN '" + str(hoy.year) + "-" + str(hoy.month) + "-1' AND '" + str(hoy.year) + "-" + str(hoy.month) + "-" + str(ultimo) +"'"
            where += " AND tt.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
        if oParam:
            if "idusuario" in oParam:
                usuario = str(oParam["idusuario"])
            if "d_fecha" not in oParam and "h_fecha" not in oParam and "fecha" not in oParam:
                hoy = date.today()
                ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
                where += " AND tt.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
            else:
                #if "i_fecha" in oParam:
                #    where += " AND tt.fecha < '" +  oParam["h_fecha"] + "'"
                if "fecha" in oParam:
                    where += "AND tt.fecha = '{}'".format(oParam["fecha"])
                if "d_fecha" in oParam:
                    where += " AND tt.fecha BETWEEN ' {} ' AND ' {} '".format(oParam["d_fecha"], oParam["h_fecha"])

        where += " AND u.idusuario = {}".format(usuario)
        data = []
        #q = qsatype.FLSqlQuery()
        #q.setTablesList(u"gt_proyectos, gt_particproyecto, aqn_user, gt_tareas, gt_timetracking")
        #q.setSelect(u"DISTINCT(t.nombre), t.idproyecto, SUM(tt.totaltiempo)")
        #q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.idproyecto=p.idproyecto INNER JOIN aqn_user u ON u.idusuario = p.idusuario INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea")
        #q.setWhere(where + " GROUP BY t.idproyecto, p.idusuario ORDER BY t.idproyecto LIMIT 20")

        q = qsatype.FLSqlQuery()
        q.setTablesList("gt_proyectos, gt_particproyecto, aqn_user, gt_tareas, gt_timetracking")
        q.setSelect("t.nombre, t.idproyecto, SUM(tt.totaltiempo)")
        q.setFrom("gt_proyectos t INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea INNER JOIN aqn_user u ON u.idusuario = tt.idusuario")
        q.setWhere(where + " GROUP BY t.idproyecto ORDER BY SUM(tt.totaltiempo) DESC LIMIT 20")
        # q.setWhere(where + " GROUP BY t.idproyecto HAVING SUM(tt.totaltiempo) > '01:00:00' ORDER BY SUM(tt.totaltiempo) DESC LIMIT 20")
        # q.setWhere(where + " GROUP BY t.idproyecto ORDER BY SUM(tt.totaltiempo) ASC LIMIT 20")

        if not q.exec_():
            return []
        if q.size() > 100:
            return []

        while q.next():
            valor = q.value(2)
            # valor = qsatype.FLUtil.quickSqlSelect("gt_timetracking", "SUM(totaltiempo)", "idusuario = " + usuario + " AND idtarea IN (Select idtarea from gt_tareas where idproyecto = '" + q.value(1) + "') ")
            nombre = q.value(0)
            if valor:
                valor = flgesttare_def.iface.seconds_to_time(valor.total_seconds(), all_in_hours=True)
                valor = flgesttare_def.iface.time_to_hours(str(valor)) or 0
            else:
                valor = 0
            codcliente = qsatype.FLUtil.sqlSelect("gt_proyectos INNER JOIN gt_clientes ON gt_clientes.idcliente = gt_proyectos.idcliente", "gt_clientes.codcliente", "gt_proyectos.idproyecto = '" + str(q.value(1)) + "'") or None
            if codcliente:
                nombre = "#" + codcliente + " " + nombre
            data.append({"name": nombre, "value": int(valor)})
        # data = [{"name": "Nombre", "value": 20, "color": "red"}, {"name": "Dos", "value": 80, "color": "orange"}]
        return {"type": "horizontalBarChart", "data": data, "innerText": True, "size": "75", "text": "Tiempo invertido en proyectos"}

    def gesttare_graficostareasporestado(self, oParam):
        usuario = qsatype.FLUtil.nameUser()
        if oParam:
            if "idusuario" in oParam:
                usuario = str(oParam["idusuario"])
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_tareas")
        q.setSelect(u"COUNT(t.codestado), t.codestado")
        q.setFrom(u"gt_tareas t")
        q.setWhere(u"t.idusuario = " + usuario + " AND not t.resuelta GROUP BY t.codestado LIMIT 20")

        if not q.exec_():
            return []
        if q.size() > 100:
            return []

        while q.next():
            valor = 0
            data.append({"name": q.value(1), "value": q.value(0)})
        # data = [{"name": "Nombre", "value": 20, "color": "red"}, {"name": "Dos", "value": 80, "color": "orange"}]
        return {"type": "pieDonutChart", "data": data, "size": 80, "innerText": True, "text": "Dristribución"}

    def gesttare_graficohorasporproyecto(self, oParam):
        tengopermiso = flgesttare_def.iface.compruebaPermisosPlan("informes_pie")
        if tengopermiso != True:
            return tengopermiso

        where = "1=1 "
        usuario = qsatype.FLUtil.nameUser()
        if not oParam:
            hoy = date.today()
            ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
            #where += " AND tt.fecha BETWEEN '" + str(hoy.year) + "-" + str(hoy.month) + "-1' AND '" + str(hoy.year) + "-" + str(hoy.month) + "-" + str(ultimo) +"'"
            where += " AND tt.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
        if oParam:
            if "idusuario" in oParam:
                usuario = str(oParam["idusuario"])
            if "d_fecha" not in oParam and "h_fecha" not in oParam and "fecha" not in oParam:
                hoy = date.today()
                ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
                where += " AND tt.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
            else:
                #if "i_fecha" in oParam:
                #    where += " AND tt.fecha < '" +  oParam["h_fecha"] + "'"
                if "fecha" in oParam:
                    where += "AND tt.fecha = '{}'".format(oParam["fecha"])
                if "d_fecha" in oParam:
                    where += " AND tt.fecha BETWEEN ' {} ' AND ' {} '".format(oParam["d_fecha"], oParam["h_fecha"])

        where += " AND u.idusuario = {}".format(usuario)
        data = []
        otros = 0
        q = qsatype.FLSqlQuery()
        q.setTablesList("gt_proyectos, gt_particproyecto, aqn_user, gt_tareas, gt_timetracking")
        q.setSelect("t.nombre, t.idproyecto, SUM(tt.totaltiempo)")
        q.setFrom("gt_proyectos t INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea INNER JOIN aqn_user u ON u.idusuario = tt.idusuario")
        q.setWhere(where + " GROUP BY t.idproyecto ORDER BY SUM(tt.totaltiempo) DESC LIMIT 20")
        # q.setWhere(where + " GROUP BY t.idproyecto HAVING SUM(tt.totaltiempo) > '01:00:00' ORDER BY SUM(tt.totaltiempo) DESC LIMIT 20")
        # q.setWhere("{} GROUP BY t.idproyecto ORDER BY SUM(tt.totaltiempo) DESC".format(where))

        # q = qsatype.FLSqlQuery()
        # q.setTablesList("gt_proyectos, gt_tareas, gt_timetracking")
        # q.setSelect("t.nombre, t.idproyecto, SUM(tt.totaltiempo)")
        # q.setFrom("gt_proyectos t INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea")
        # q.setWhere("{} GROUP BY t.idproyecto ORDER BY t.idproyecto".format(where))

        if not q.exec_():
            return []
        if q.size() > 100:
            return []

        # total = qsatype.FLUtil.sqlSelect("gt_timetracking tt INNER JOIN aqn_user u ON u.idusuario = tt.idusuario", "SUM(tt.totaltiempo)", where)

        total = qsatype.FLUtil.sqlSelect("gt_proyectos t INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea INNER JOIN aqn_user u ON u.idusuario = tt.idusuario", "SUM(tt.totaltiempo)", where)

        if total:
            total = flgesttare_def.iface.seconds_to_time(total.total_seconds(), all_in_hours=True)
            total = flgesttare_def.iface.time_to_hours(str(total))
        else:
            total = 0


        i = 0
        while q.next():
            valor = q.value(2)
            # valor = qsatype.FLUtil.quickSqlSelect("gt_timetracking", "SUM(totaltiempo)", "idusuario = " + usuario + " AND idtarea IN (Select idtarea from gt_tareas where idproyecto = '" + q.value(1) + "') ")
            if valor:
                valor = flgesttare_def.iface.seconds_to_time(valor.total_seconds(), all_in_hours=True)
                valor = flgesttare_def.iface.time_to_hours(str(valor))
            else:
                valor = 0

            if i > 7:
                otros += valor
            else:
                porcentaje = 0
                if total != 0 and total != None:
                    porcentaje = 100*(valor/total)
                nombre = q.value(0)
                codcliente = qsatype.FLUtil.sqlSelect("gt_proyectos INNER JOIN gt_clientes ON gt_clientes.idcliente = gt_proyectos.idcliente", "gt_clientes.codcliente", "gt_proyectos.idproyecto = '" + str(q.value(1)) + "'") or None
                if codcliente:
                    nombre = "#" + codcliente + " " + nombre
                data.append({"name": nombre, "value": round(porcentaje,2)})
            i = i+1
            if i == q.size() and otros > 0:
                if total != 0 and total != None:
                    porcentaje = 100*(otros/total)
                data.append({"name": "Otros Proyectos", "value": round(porcentaje,2)})

        return {"type": "pieDonutChart", "data": data, "size": 80, "innerText": True, "text": "Distribución del tiempo en proyectos"}

    def gesttare_calculaTareasCompletadas(self, oParam):
        where = "1=1"
        usuario = qsatype.FLUtil.nameUser()

        locale.setlocale(locale.LC_ALL, '')

        if not oParam:
            hoy = date.today()
            ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
            where += " AND at.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
        if oParam:
            if "idusuario" in oParam:
                usuario = str(oParam["idusuario"])
            if "d_fecha" not in oParam and "h_fecha" not in oParam and "fecha" not in oParam:
                hoy = date.today()
                ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
                where += " AND at.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
            else:
                if "fecha" in oParam:
                    where += "AND at.fecha = '{}'".format(oParam["fecha"])
                if "d_fecha" in oParam:
                    where += " AND at.fecha BETWEEN ' {} ' AND ' {} '".format(oParam["d_fecha"], oParam["h_fecha"])
        whereCompletadas = where + " AND ta.idusuario = '" + usuario + "'AND ta.resuelta = 'true' AND at.tipo='resuelta'"
        tareasCompletadas = qsatype.FLUtil.sqlSelect("gt_tareas ta LEFT JOIN gt_actualizaciones at ON ta.idtarea = at.idobjeto::INTEGER", "COUNT(ta.idtarea)", whereCompletadas) or 0
        return tareasCompletadas

    def gesttare_calculaTareasCompletadasRanking(self, oParam):
        where = "1=1"
        usuario = qsatype.FLUtil.nameUser()

        locale.setlocale(locale.LC_ALL, '')

        if not oParam:
            hoy = date.today()
            ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
            where += " AND at.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
        if oParam:
            if "idusuario" in oParam:
                usuario = str(oParam["idusuario"])
            if "d_fecha" not in oParam and "h_fecha" not in oParam and "fecha" not in oParam:
                hoy = date.today()
                ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
                where += " AND at.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
            else:
                if "fecha" in oParam:
                    where += "AND at.fecha = '{}'".format(oParam["fecha"])
                if "d_fecha" in oParam:
                    where += " AND at.fecha BETWEEN ' {} ' AND ' {} '".format(oParam["d_fecha"], oParam["h_fecha"])
        id_compania = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(usuario))
        whereCompletadas = where + " AND u. idcompany = {} AND ta.resuelta = 'true' AND at.tipo='resuelta'".format(id_compania)
        # tareasCompletadas = qsatype.FLUtil.sqlSelect("gt_tareas ta LEFT JOIN gt_actualizaciones at ON ta.idtarea = at.idobjeto::INTEGER", "COUNT(ta.idtarea)", whereCompletadas) or 0

        ranking_completadas = []

        q = qsatype.FLSqlQuery()
        q.setTablesList(" gt_tareas, gt_actualizaciones, aqn_user")
        q.setSelect("COUNT(ta.idtarea), u.idusuario")
        q.setFrom("gt_tareas ta LEFT JOIN gt_actualizaciones at ON ta.idtarea = at.idobjeto::INTEGER INNER JOIN aqn_user u ON ta.idusuario = u.idusuario")
        q.setWhere(whereCompletadas + " GROUP BY u.idusuario ORDER BY COUNT(ta.idtarea) DESC")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 100:
            print("sale por aqui")
            return []

        while q.next():
            # descripcion = str(q.value(2)) + "€ " + q.value(1)
            ranking_completadas.append(q.value(1))

        if int(usuario) in ranking_completadas:
            posicion_completadas = ranking_completadas.index(int(usuario))
            posicion_completadas = "#" + str(posicion_completadas + 1)
        else:
            posicion_completadas = "-"
        return posicion_completadas

    def gesttare_cajasinfo(self, oParam):
        horasStyle = {
            "border": "1px solid #dfdfdf",
            "backgroundColor": "white",
            "color": "grey",
            "marginBottom": "5px"
        }

        presupuestoStyle = {
            "backgroundColor": "#bababa",
            "color": "#ffffff",
            "marginBottom": "5px"
        }

        rentabilidadStyle = {
            "backgroundImage": "linear-gradient(to right, #e79b21, #ffc68d)",
            "color": "#ffffff",
            "marginBottom": "5px"
        }

        rankingStyle = {
            "backgroundImage": "linear-gradient(to left, #89e3dc, #4abed8)",
            "color": "#ffffff",
            "marginBottom": "5px"
        }


        tengopermiso = flgesttare_def.iface.compruebaPermisosPlan("informes_info")
        if tengopermiso != True:
            return tengopermiso

        where = "1=1"
        where_horas_trabajadas = "1=1"
        usuario = qsatype.FLUtil.nameUser()

        locale.setlocale(locale.LC_ALL, '')

        if not oParam:
            hoy = date.today()
            ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
            #where += " AND tt.fecha BETWEEN '" + str(hoy.year) + "-" + str(hoy.month) + "-1' AND '" + str(hoy.year) + "-" + str(hoy.month) + "-" + str(ultimo) +"'"
            where += " AND tt.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
            where_horas_trabajadas += " AND gt_controldiario.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
        if oParam:
            if "idusuario" in oParam:
                usuario = str(oParam["idusuario"])
            if "d_fecha" not in oParam and "h_fecha" not in oParam and "fecha" not in oParam:
                hoy = date.today()
                ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
                where += " AND tt.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
                where_horas_trabajadas += " AND gt_controldiario.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
            else:
                #if "i_fecha" in oParam:
                #    where += " AND tt.fecha < '" +  oParam["h_fecha"] + "'"
                if "fecha" in oParam:
                    where += "AND tt.fecha = '{}'".format(oParam["fecha"])
                    where_horas_trabajadas += "AND gt_controldiario.fecha = '{}'".format(oParam["fecha"])
                if "d_fecha" in oParam:
                    where += " AND tt.fecha BETWEEN ' {} ' AND ' {} '".format(oParam["d_fecha"], oParam["h_fecha"])
                    where_horas_trabajadas += " AND gt_controldiario.fecha BETWEEN ' {} ' AND ' {} '".format(oParam["d_fecha"], oParam["h_fecha"])

        # where += " AND tt.idusuario = {}".format(usuario)
        # tiempo = qsatype.FLUtil.sqlSelect("gt_timetracking tt", "SUM(tt.totaltiempo)", where)
        id_compania = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(usuario))
        where_ranking_trackeadas = where + " AND u.idcompany = {}".format(id_compania)
        where += " AND tt.idusuario = {}".format(usuario)
        where_horas_trabajadas_ranking = where_horas_trabajadas + " AND aqn_user.idcompany = {}".format(id_compania)
        where_horas_trabajadas += " AND gt_controldiario.idusuario = {}".format(usuario)


        # tiempo = qsatype.FLUtil.sqlSelect("gt_timetracking tt INNER JOIN aqn_user u ON u.idusuario = tt.idusuario", "SUM(tt.totaltiempo)", where)
        tiempo = qsatype.FLUtil.sqlSelect("gt_proyectos t INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea INNER JOIN aqn_user u ON u.idusuario = tt.idusuario", "SUM(tt.totaltiempo)", where)

        totalPresupuesto = 0
        totalCostes = 0
        rentabilidad = 0
        tareasCompletadas = 0
        TareasProduccion = 0


        whereProduccion = where + " AND tt.totaltiempo != '00:00:00'"

        #tareasCompletadas = qsatype.FLUtil.sqlSelect("gt_proyectos t INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea  INNER JOIN aqn_user u ON u.idusuario =tt.idusuario ", "COUNT(u.idusuario)", whereCompletadas)
        tareasCompletadas = self.iface.calculaTareasCompletadas(oParam)

        # tareasProduccion =  qsatype.FLUtil.sqlSelect("gt_proyectos t INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea  INNER JOIN aqn_user u ON u.idusuario = tt.idusuario ", "COUNT(u.idusuario)", whereProduccion)

        tareasProduccion =  qsatype.FLUtil.sqlSelect("gt_tareas ta INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea", "COUNT(DISTINCT(tt.idtarea))", whereProduccion)
        if tareasCompletadas == None:
            tareasCompletadas = 0

        if tareasProduccion == None:
            tareasProduccion = 0


        if tiempo:
            tiempo = flgesttare_def.iface.seconds_to_time(tiempo.total_seconds(), all_in_hours=True)
            tiempo = flgesttare_def.iface.formatearTotalTiempo(tiempo).split(":")[0]
            if tiempo[0] == "0":
                tiempo = tiempo[1]
        else:
            tiempo = "0"



        horas_trabajadas =  qsatype.FLUtil.sqlSelect("gt_controldiario INNER JOIN aqn_user ON gt_controldiario.idusuario = aqn_user.idusuario", "SUM(gt_controldiario.totaltiempo)", where_horas_trabajadas)

        if horas_trabajadas:
            horas_trabajadas = flgesttare_def.iface.seconds_to_time(int(horas_trabajadas), all_in_hours=True)
            horas_trabajadas = flgesttare_def.iface.formatearTotalTiempo(horas_trabajadas).split(":")[0]
            if horas_trabajadas[0] == "0":
                horas_trabajadas = horas_trabajadas[1]
        else:
            horas_trabajadas = "0"

        if int(horas_trabajadas) != 0:
            porcentaje_efectivo = (100 * int(tiempo)) / int(horas_trabajadas)

            if porcentaje_efectivo != 0:
                porcentaje_efectivo = str(round(porcentaje_efectivo, 2)) + "%"
            else:
                porcentaje_efectivo = "-"
        else:
            porcentaje_efectivo = "-"


        numero_proyectos = qsatype.FLUtil.sqlSelect("gt_proyectos t INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea INNER JOIN aqn_user u ON u.idusuario = tt.idusuario", "COUNT(DISTINCT(t.idproyecto))", where)

        numero_hitos = qsatype.FLUtil.sqlSelect("gt_proyectos t INNER JOIN gt_hitosproyecto h ON t.idproyecto = h.idproyecto INNER JOIN gt_tareas ta ON h.idhito = ta.idhito INNER JOIN gt_timetracking tt ON ta.idtarea = tt.idtarea INNER JOIN aqn_user u ON u.idusuario = tt.idusuario", "COUNT(DISTINCT(h.idhito))", where)

        # ranking_trackeadas = qsatype.FLUtil.sqlSelect("gt_proyectos t INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea INNER JOIN aqn_user u ON u.idusuario = tt.idusuario", "SUM(tt.totaltiempo)", where)
        # ranking_trackeadas = []
        # q = qsatype.FLSqlQuery()
        # q.setTablesList("gt_proyectos, gt_tareas, gt_timetracking, aqn_user")
        # q.setSelect("SUM(tt.totaltiempo), u.idusuario")
        # q.setFrom("gt_proyectos t INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea INNER JOIN aqn_user u ON u.idusuario = tt.idusuario")
        # q.setWhere(where_ranking_trackeadas + " GROUP BY u.idusuario ORDER BY SUM(tt.totaltiempo) DESC")

        # if not q.exec_():
        #     print("Error inesperado")
        #     return []
        # if q.size() > 100:
        #     print("sale por aqui")
        #     return []

        # while q.next():
        #     print("el valor es: ",q.value(0))
        #     # descripcion = str(q.value(2)) + "€ " + q.value(1)
        #     ranking_trackeadas.append(q.value(1))

        # if int(usuario) in ranking_trackeadas:
        #     posicion_trackeadas = ranking_trackeadas.index(int(usuario))
        #     posicion_trackeadas = "#" + str(posicion_trackeadas + 1)
        # else:
        #     posicion_trackeadas = "-"


        # ranking_produccion = []
        # q = qsatype.FLSqlQuery()
        # q.setTablesList(" gt_tareas, gt_timetracking, aqn_user")
        # q.setSelect("COUNT(DISTINCT(tt.idtarea)), u.idusuario")
        # q.setFrom("gt_tareas ta INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea INNER JOIN aqn_user u ON u.idusuario = tt.idusuario")
        # q.setWhere(where_ranking_trackeadas + " GROUP BY u.idusuario ORDER BY COUNT(DISTINCT(tt.idtarea)) DESC")

        # if not q.exec_():
        #     print("Error inesperado")
        #     return []
        # if q.size() > 100:
        #     print("sale por aqui")
        #     return []

        # while q.next():
        #     # descripcion = str(q.value(2)) + "€ " + q.value(1)
        #     ranking_produccion.append(q.value(1))

        # if int(usuario) in ranking_produccion:
        #     posicion_produccion = ranking_produccion.index(int(usuario))
        #     posicion_produccion = "#" + str(posicion_produccion + 1)
        # else:
        #     posicion_produccion = "-"

        q = qsatype.FLSqlQuery()
        q.setTablesList("gt_proyectos, gt_tareas, gt_timetracking, aqn_user")
        q.setSelect("SUM(tt.totaltiempo), u.idusuario")
        q.setFrom("gt_proyectos t INNER JOIN gt_tareas ta ON t.idproyecto=ta.idproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea INNER JOIN aqn_user u ON u.idusuario = tt.idusuario")
        q.setWhere(where_ranking_trackeadas + " GROUP BY u.idusuario ORDER BY SUM(tt.totaltiempo) DESC")

        q2 = qsatype.FLSqlQuery()
        q2.setTablesList("gt_controldiario, aqn_user")
        q2.setSelect("SUM(gt_controldiario.totaltiempo), aqn_user.idusuario")
        q2.setFrom("gt_controldiario INNER JOIN aqn_user ON gt_controldiario.idusuario = aqn_user.idusuario")
        q2.setWhere(where_horas_trabajadas_ranking + " GROUP BY  aqn_user.idusuario ORDER BY SUM(gt_controldiario.totaltiempo) DESC")

        if not q.exec_():
            print("Error inesperado")
            return []

        if not q2.exec_():
            print("Error inesperado")
            return []

        if q.size() > 100:
            print("sale por aqui")
            return []

        if q2.size() > 100:
            print("sale por aqui")
            return []

        usuarios = {}
        while q2.next():
            horas_trabajadas_q = q2.value(0)
            if horas_trabajadas_q:
                horas_trabajadas_q = flgesttare_def.iface.seconds_to_time(int(horas_trabajadas_q), all_in_hours=True)

                horas_trabajadas_q = flgesttare_def.iface.formatearTotalTiempo(horas_trabajadas_q).split(":")[0]
                if horas_trabajadas_q[0] == "0":
                    horas_trabajadas_q = horas_trabajadas_q[1]
            else:
                horas_trabajadas_q = "0"
            usuarios[q2.value(1)] = { "horas_trabajadas": horas_trabajadas_q, "horas_trackeadas": 0, "porcentaje": 0 }

        porcentajes = {}
        while q.next():
            horas_trackeadas = q.value(0)
            if horas_trackeadas:
                horas_trackeadas = flgesttare_def.iface.seconds_to_time(horas_trackeadas.total_seconds(), all_in_hours=True)

                horas_trackeadas = flgesttare_def.iface.formatearTotalTiempo(horas_trackeadas).split(":")[0]
                if horas_trackeadas[0] == "0":
                    horas_trackeadas = horas_trackeadas[1]
            else:
                horas_trackeadas = "0"
            id_usuario = q.value(1)
            if id_usuario not in usuarios:
                continue

            usuarios[id_usuario]["horas_trackeadas"] = horas_trackeadas
            # print("el valor Trackeadas es: ", usuarios[id_usuario]["horas_trackeadas"])
            # print("el valor horas_trabajadas es: ", usuarios[id_usuario]["horas_trabajadas"])
            if int(usuarios[id_usuario]["horas_trabajadas"]) != 0:
                porcentajes[id_usuario] =  (100 * int(usuarios[id_usuario]["horas_trackeadas"])) / int(usuarios[id_usuario]["horas_trabajadas"])
            else:
                porcentajes[id_usuario] = 0



        contador = 1

        if int(usuario) in usuarios:
            sort_porcentajes = sorted(porcentajes.items(), key=lambda x: x[1], reverse=True)
            for i in sort_porcentajes:
                if i[0] == int(usuario):
                    posicion_porcentaje = "#" + str(contador)
                    contador = 0
                else:
                    contador = contador + 1
                # print(type(i[0]), i[1])
        else:
            posicion_porcentaje = "-"




        # if int(usuario) in sort_porcentajes:
        #     posicion_porcentaje = sort_porcentajes.index(int(usuario))
        #     posicion_porcentaje = "#" + str(posicion_porcentaje + 1)
        # else:
        #     posicion_porcentaje = "-"


        posicion_completadas = self.iface.calculaTareasCompletadasRanking(oParam)

        data = [{"name": "Nº Horas trabajadas", "value": horas_trabajadas, "style": horasStyle}, {"name": "Nº Horas Trackeadas", "value": tiempo, "style": presupuestoStyle}, {"name": "% horas Efectivas", "value": porcentaje_efectivo, "style": rentabilidadStyle}, {"name": "Nº Tareas En Producción", "value": tareasProduccion, "style" :horasStyle}, {"name": "Nº Proyectos en producción", "value": numero_proyectos, "style": presupuestoStyle}, {"name": "Nº Tareas Completadas", "value": tareasCompletadas, "style": rentabilidadStyle}, {"name": "horas efectivas", "value": posicion_porcentaje, "style": rankingStyle}, {"name": "tareas completadas", "value": posicion_completadas, "style": rankingStyle}]
        return {"type": "labelInfo", "data": data}

    def gesttare_queryGrid_tareasMasTiempo(self, model, filters):

        where = "1=1"
        usuario = qsatype.FLUtil.nameUser()

        if not filters:
            hoy = date.today()
            ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
            where += " AND tt.fecha BETWEEN '" + str(hoy.year) + "-" + str(hoy.month) + "-1' AND '" + str(hoy.year) + "-" + str(hoy.month) + "-" + str(ultimo) +"'"
        if filters:
            if "[idusuario]" in filters and filters["[idusuario]"] != "":
                usuario ="'{}'".format(filters["[idusuario]"])
            if "[d_fecha]" in filters and filters["[d_fecha]"] == "" and "[h_fecha]" in filters and filters["[h_fecha]"] == "" and "[fecha]" in filters and filters["[fecha]"] == "":
                hoy = date.today()
                ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
                where += " AND tt.fecha BETWEEN '{}-{}-1' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.month), str(hoy.year), str(hoy.month), str(ultimo))
            else:
                if "[fecha]" in filters and filters["[fecha]"] != "":
                    where += "AND tt.fecha = '{}'".format(filters["[fecha]"])
                if "[d_fecha]" in filters and filters["[d_fecha]"] != "":
                    where += " AND tt.fecha BETWEEN ' {} ' AND ' {} '".format(filters["[d_fecha]"], filters["[h_fecha]"])

        where += " AND a.idusuario = {}".format(usuario)

        query = {}
        query["tablesList"] = ("gt_proyectos, gt_tareas, gt_timetracking, aqn_user")
        query["select"] = ("t.idtarea, a.usuario, tt.totaltiempo, t.nombre, tt.fecha, p.nombre")
        query["from"] = ("aqn_user a INNER JOIN gt_particproyecto pp ON a.idusuario = pp.idusuario INNER JOIN gt_proyectos p ON pp.idproyecto = p.idproyecto INNER JOIN gt_tareas t ON p.idproyecto = t.idproyecto INNER JOIN gt_timetracking tt ON t.idtarea = tt.idtarea")
        query["where"] = "{} AND tt.totaltiempo < (SELECT MAX(tt.totaltiempo) FROM gt_timetracking tt)".format(where)
        query["orderby"] = (" tt.totaltiempo DESC")

        return query


    def gesttare_calculaGraficosAnalisis(self, oParam):
        response = []
        cajasinfo = self.iface.cajasinfo(oParam)
        response.append(cajasinfo)
        proyectosportiempo = self.iface.graficoproyectosportiempo(oParam)
        response.append(proyectosportiempo)
        # tareasporestado = self.iface.graficostareasporestado(oParam)
        # response.append(tareasporestado)
        horasporproyecto = self.iface.graficohorasporproyecto(oParam)
        response.append(horasporproyecto)
        return response

    def gesttare_generaAnalisisGraphic(self, model, template):
        return self.iface.calculaGraficosAnalisis({})

    def gesttare_getAnalisisGraphic(self, oParam):
        return self.iface.calculaGraficosAnalisis(oParam)

    def gesttare_drawif_idusuariofilter(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        isSuperuser = qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(usuario))
        if not isSuperuser:
            return "hidden"
        return True

    def gesttare_color_usuario(self, model):
        # print(model['aqn_user.usuario'])
        # if (model['aqn_user.usuario']):
        #     return "usuario"

        return "usuarioAqn"

    def gesttare_dameEmailCreaAnotacion(self, oParam, cursor):
        response = {}
        print("___________________________________")
        if "email" not in oParam:
            # "Javier Cantos Cañete" <javier.cantos@makinando.es>
            # val = str(cursor.valueBuffer("idproyecto")) + "@convert.dailyjob.io"
            apellidos = cursor.valueBuffer("apellidos") or ""
            val = '"' + str(cursor.valueBuffer("nombre")) + ' ' + str(apellidos) + '" <' + str(cursor.valueBuffer("usuario")) + "@convert.dailyjob.io" + '>'
            response['status'] = -1
            response['data'] = {}
            response['buttons'] = False
            response['title'] = "Copiar en el portapapeles: Ctrl+C"
            response['params'] = [
                {
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "rel": "gt_proyectos",
                    "style": {
                        "width": "100%"
                    },
                    "tipo": 3,
                    "verbose_name": "Email",
                    "label": "Email",
                    "key": "idusuario",
                    "disabled": False,
                    "value": val,
                    "validaciones": None,
                    "required": False,
                    "select": True
                }
            ]
            return response
        else:
            return True

    # def gesttare_activar_nomenclatura(self, cursor):
    #     usuario = qsatype.FLUtil.nameUser()
    #     tiene_config = qsatype.FLUtil.sqlSelect("gt_configuser", "idusuario", "idusuario = " + str(usuario))
    #     response = {}
    #     if not tiene_config:
    #         cur_config = qsatype.FLSqlCursor("gt_configuser")
    #         cur_config.setModeAccess(cur_config.Insert)
    #         cur_config.refreshBuffer()

    #         cur_config.setValueBuffer("idusuario", str(usuario))
    #         cur_config.setValueBuffer("nomenclatura", True)
    #         if not cur_config.commitBuffer():
    #             print("Ocurrió un error al insertar el registro de gt_configuser")
    #             return False
    #     else:
    #         cur_config = qsatype.FLSqlCursor("gt_configuser")
    #         cur_config.select("idusuario = {}".format(str(usuario)))

    #         if cur_track.first():
    #             cur_config = qsatype.FLSqlCursor("gt_configuser")
    #             cur_config.setModeAccess(cur_config.Edit)
    #             cur_config.refreshBuffer()

    #             cur_config.setValueBuffer("nomenclatura", True)
    #             if not cur_config.commitBuffer():
    #                 print("Ocurrió un error al actualizar el registro de gt_configuser")
    #                 return False

    #     # sql = "INSERT INTO gt_configuser(idusuario, nomenclatura) VALUES (" + str(usuario) + ")"

    #     # qsatype.FLUtil.execSql(sql)

    #     response["resul"] = True
    #     response["msg"] = "Nomenclatura Activada"
    #     return response

    # def gesttare_desactivar_nomenclatura(self, cursor):
    #     usuario = qsatype.FLUtil.nameUser()
    #     tiene_config = qsatype.FLUtil.sqlSelect("gt_configuser", "idusuario", "idusuario = " + str(usuario))
    #     response = {}
    #     if not tiene_config:
    #         cur_config = qsatype.FLSqlCursor("gt_configuser")
    #         cur_config.setModeAccess(cur_config.Insert)
    #         cur_config.refreshBuffer()

    #         cur_config.setValueBuffer("idusuario", str(usuario))
    #         cur_config.setValueBuffer("nomenclatura", False)
    #         if not cur_config.commitBuffer():
    #             print("Ocurrió un error al insertar el registro de gt_configuser")
    #             return False
    #     else:
    #         cur_config = qsatype.FLSqlCursor("gt_configuser")
    #         cur_config.select("idusuario = {}".format(str(usuario)))

    #         if cur_track.first():
    #             cur_config = qsatype.FLSqlCursor("gt_configuser")
    #             cur_config.setModeAccess(cur_config.Edit)
    #             cur_config.refreshBuffer()

    #             cur_config.setValueBuffer("nomenclatura", False)
    #             if not cur_config.commitBuffer():
    #                 print("Ocurrió un error al actualizar el registro de gt_configuser")
    #                 return False

    #     # sql = "INSERT INTO gt_configuser(idusuario, nomenclatura) VALUES (" + str(usuario) + ")"

    #     # qsatype.FLUtil.execSql(sql)

    #     response["resul"] = True
    #     response["msg"] = "Nomenclatura Activada"
    #     return response

    # def get_config_usuario(self, usuario):
    #     cur_config = new FLSqlCursor("gt_configuser")
    #     cur_config.select("idusuario = " + str(usuario))
    #     if not cur_config.first():
    #         cur_config.setModeAccess(cur_config.Insert)
    #         refreshBuffer
    #         setValueBuffer("idusuario")
    #         commitBuffer
    #     else:
    #         cur_config.setModeAccess(cur_config.Insert)
    #         refreshBuffer
    #     return  {
    #         "nomenclatura": cursor.valueBuffer("nomenclatura")
    #     }


    # def gesttare_drawif_nomenclatura_activar(self, cursor):
    #     print("????")
    #     usuario = qsatype.FLUtil.nameUser()
    #     config_usuario = self.get_config_usuario(usuario)
    #     tiene_nomenclatura = qsatype.FLUtil.sqlSelect("gt_configuser", "nomenclatura", "idusuario = " + str(usuario))
    #     if tiene_nomenclatura:
    #         return "hidden"

    # def gesttare_drawif_nomenclatura_desactivar(self, cursor):
    #     print("????2")
    #     usuario = qsatype.FLUtil.nameUser()
    #     tiene_nomenclatura = qsatype.FLUtil.sqlSelect("gt_configuser", "nomenclatura", "idusuario = " + str(usuario))
    #     if not tiene_nomenclatura:
    #         return "hidden"

    def __init__(self, context=None):
        super().__init__(context)

    def checkDrawUser(self, cursor):
        return self.ctx.gesttare_checkDrawUser(cursor)

    def activar_nomenclatura(self, cursor):
        return self.ctx.gesttare_activar_nomenclatura(cursor)

    def drawif_nomenclatura_activar(self, cursor):
        return self.ctx.gesttare_drawif_nomenclatura_activar(cursor)

    def drawif_nomenclatura_desactivar(self, cursor):
        return self.ctx.gesttare_nomenclatura_desactivar(cursor)

    def checkResponsableDraw(self, cursor):
        return self.ctx.gesttare_checkResponsableDraw(cursor)

    def checkCambiaPassword(self, cursor):
        return self.ctx.gesttare_checkCambiaPassword(cursor)

    def getUsuariosProyecto(self, oParam):
        return self.ctx.gesttare_getUsuariosProyecto(oParam)

    def getParticipantesProyecto(self, oParam):
        return self.ctx.gesttare_getParticipantesProyecto(oParam)

    def getParticProyectosUsu(self, oParam):
        return self.ctx.gesttare_getParticProyectosUsu(oParam)

    def getUsuTutelados(self, oParam):
        return self.ctx.gesttare_getUsuTutelados(oParam)

    def getParticCompaniaUsu(self, oParam):
        return self.ctx.gesttare_getParticCompaniaUsu(oParam)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def activar(self, model, oParam, cursor):
        return self.ctx.gesttare_activar(model, oParam, cursor)

    def check_permissions(self, model, prefix, pk, template, acl, accion=None):
        return self.ctx.gesttare_check_permissions(model, prefix, pk, template, acl, accion)

    def generaAnalisisGraphic(self, model, template):
        return self.ctx.gesttare_generaAnalisisGraphic(model, template)

    def getAnalisisGraphic(self, oParam):
        return self.ctx.gesttare_getAnalisisGraphic(oParam)

    def calculaGraficosAnalisis(self, oParam):
        return self.ctx.gesttare_calculaGraficosAnalisis(oParam)

    def graficoproyectosportiempo(self, oParam):
        return self.ctx.gesttare_graficoproyectosportiempo(oParam)

    def graficostareasporestado(self, oParam):
        return self.ctx.gesttare_graficostareasporestado(oParam)

    def graficohorasporproyecto(self, oParam):
        return self.ctx.gesttare_graficohorasporproyecto(oParam)

    def calculaTareasCompletadas(self, oParam):
        return self.ctx.gesttare_calculaTareasCompletadas(oParam)

    def calculaTareasCompletadasRanking(self, oParam):
        return self.ctx.gesttare_calculaTareasCompletadasRanking(oParam)

    def cajasinfo(self, oParam):
        return self.ctx.gesttare_cajasinfo(oParam)

    def queryGrid_tareasMasTiempo(self, model, filters):
        return self.ctx.gesttare_queryGrid_tareasMasTiempo(model, filters)

    def drawif_idusuariofilter(self, cursor):
        return self.ctx.gesttare_drawif_idusuariofilter(cursor)

    def field_nombre(self, model):
        return self.ctx.gesttare_field_nombre(model)

    def field_nombreform(self, model):
        return self.ctx.gesttare_field_nombreform(model)

    def color_usuario(self, model):
        return self.ctx.gesttare_color_usuario(model)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def dameEmailCreaAnotacion(self, oParam, cursor):
        return self.ctx.gesttare_dameEmailCreaAnotacion(oParam, cursor)

    def field_completaIcon(self, model):
        return self.ctx.gesttare_field_completaIcon(model)

    def field_completaTitle(self, model):
        return self.ctx.gesttare_field_completaTitle(model)

