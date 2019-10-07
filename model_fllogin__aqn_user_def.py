
# @class_declaration gesttare #
from models.flgesttare import flgesttare_def
import datetime
from datetime import date
import calendar
import locale

class gesttare(yblogin):

    def gesttare_getUsuariosProyecto(self, oParam):
        data = []
        if "codproyecto" not in oParam:
            return data
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_proyectos, gt_particproyecto, aqn_user")
        q.setSelect(u"p.idusuario, u.usuario")
        q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.codproyecto=p.codproyecto INNER JOIN aqn_user u ON u.idusuario =p.idusuario")
        q.setWhere(u"t.codproyecto = '" + str(oParam['codproyecto']) + "' AND (UPPER(u.usuario) LIKE UPPER('%" + oParam["val"] + "%') OR UPPER(u.email) LIKE UPPER('%" + oParam["val"] + "%')) AND u.activo  ORDER BY u.usuario LIMIT 7")

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
        q.setFrom(u"gt_tareas t LEFT JOIN gt_particproyecto p ON t.codproyecto=p.codproyecto INNER JOIN aqn_user u ON u.idusuario =p.idusuario")
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

    def gesttare_getParticProyectosUsu(self, oParam):
        usuario = qsatype.FLUtil.nameUser()
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_particproyecto, aqn_user")
        q.setSelect(u"DISTINCT(p.idusuario), u.usuario")
        q.setFrom(u"gt_particproyecto p INNER JOIN aqn_user u ON p.idusuario = u.idusuario")
        q.setWhere(u"p.codproyecto in (select p.codproyecto from gt_particproyecto p INNER JOIN aqn_user u  ON p.idusuario = u.idusuario where p.idusuario = '" + str(usuario) + "') AND UPPER(u.usuario) LIKE UPPER('%" + oParam["val"] + "%') AND u.activo  ORDER BY u.usuario LIMIT 7")
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

    def gesttare_desactivar_usuario(self, model, oParam, cursor):
        response = {}
        if "confirmacion" in oParam and oParam["confirmacion"]:
            cursor.setModeAccess(cursor.Edit)
            cursor.refreshBuffer()
            cursor.setValueBuffer("activo", False)
            if not cursor.commitBuffer():
                response["status"] = 1
                response["msg"] = "No se puedo desactivar usuario"
                return response
            if not qsatype.FLUtil.sqlDelete(u"gt_partictarea", ustr(u"idusuario = ", cursor.valueBuffer("idusuario"))):
                response["status"] = 1
                response["msg"] = "No se puedo desactivar usuario"
                return response
            if not qsatype.FLUtil.sqlDelete(u"gt_particproyecto", ustr(u"idusuario = ", cursor.valueBuffer("idusuario"))):
                response["status"] = 1
                response["msg"] = "No se puedo desactivar usuario"
                return response
            response["resul"] = True
            response["msg"] = "Usuario " + cursor.valueBuffer("usuario") + " desactivado"
            return response
        response["status"] = 2
        response["confirm"] = "¿Seguro que quieres desactivar usuario?"
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

    def gesttare_check_permissions(self, model, prefix, pk, template, acl, accion):
        usuario = qsatype.FLUtil.nameUser()
        isadmin = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        if pk == usuario:
            return True
        elif not isadmin and accion is None:
            return False
        return True

    def gesttare_graficoproyectosportiempo(self, oParam):
        where = "1=1 "
        usuario = qsatype.FLUtil.nameUser()
        print(oParam)
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
        #q.setSelect(u"DISTINCT(t.nombre), t.codproyecto, SUM(tt.totaltiempo)")
        #q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.codproyecto=p.codproyecto INNER JOIN aqn_user u ON u.idusuario = p.idusuario INNER JOIN gt_tareas ta ON t.codproyecto=ta.codproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea")
        #q.setWhere(where + " GROUP BY t.codproyecto, p.idusuario ORDER BY t.codproyecto LIMIT 20")

        q = qsatype.FLSqlQuery()
        q.setTablesList("gt_proyectos, gt_particproyecto, aqn_user, gt_tareas, gt_timetracking")
        q.setSelect("t.nombre, t.codproyecto, SUM(tt.totaltiempo)")
        q.setFrom("gt_proyectos t LEFT JOIN gt_particproyecto p ON t.codproyecto=p.codproyecto INNER JOIN aqn_user u ON u.idusuario = p.idusuario INNER JOIN gt_tareas ta ON t.codproyecto=ta.codproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea")
        q.setWhere(where + " GROUP BY t.codproyecto ORDER BY t.codproyecto LIMIT 20")

        if not q.exec_():
            return []
        if q.size() > 100:
            return []

        while q.next():
            valor = q.value(2)
            # valor = qsatype.FLUtil.quickSqlSelect("gt_timetracking", "SUM(totaltiempo)", "idusuario = " + usuario + " AND idtarea IN (Select idtarea from gt_tareas where codproyecto = '" + q.value(1) + "') ")
            if valor:
                valor = flgesttare_def.iface.seconds_to_time(valor.total_seconds(), all_in_hours=True)
                valor = flgesttare_def.iface.time_to_hours(str(valor))
            else:
                valor = 0
            data.append({"name": q.value(0), "value": int(valor)})
        # data = [{"name": "Nombre", "value": 20, "color": "red"}, {"name": "Dos", "value": 80, "color": "orange"}]
        return {"type": "horizontalBarChart", "data": data, "innerText": True, "size": "75"}

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
        return {"type": "pieDonutChart", "data": data, "size": 100, "innerText": True}

    def gesttare_graficohorasporproyecto(self, oParam):
        where = "1=1 "
        usuario = qsatype.FLUtil.nameUser()
        print(oParam)
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

        where += " AND tt.idusuario = {}".format(usuario)
        data = []
        otros = 0
        #q = qsatype.FLSqlQuery()
        #q.setTablesList(u"gt_proyectos, gt_particproyecto, aqn_user, gt_tareas, gt_timetracking")
        #q.setSelect(u"DISTINCT(t.nombre), t.codproyecto, SUM(tt.totaltiempo)")
        #q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.codproyecto=p.codproyecto INNER JOIN aqn_user u ON u.idusuario = p.idusuario INNER JOIN gt_tareas ta ON t.codproyecto=ta.codproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea")
        #q.setWhere("{} GROUP BY t.codproyecto, p.idusuario ORDER BY t.codproyecto".format(where))

        q = qsatype.FLSqlQuery()
        q.setTablesList("gt_proyectos, gt_tareas, gt_timetracking")
        q.setSelect("t.nombre, t.codproyecto, SUM(tt.totaltiempo)")
        q.setFrom("gt_proyectos t INNER JOIN gt_tareas ta ON t.codproyecto=ta.codproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea")
        q.setWhere("{} GROUP BY t.codproyecto ORDER BY t.codproyecto".format(where))

        if not q.exec_():
            return []
        if q.size() > 100:
            return []

        total = qsatype.FLUtil.sqlSelect("gt_timetracking tt INNER JOIN aqn_user u ON u.idusuario = tt.idusuario", "SUM(tt.totaltiempo)", where)

        if total:
            total = flgesttare_def.iface.seconds_to_time(total.total_seconds(), all_in_hours=True)
            total = flgesttare_def.iface.time_to_hours(str(total))
        else:
            total = 0


        i = 0
        while q.next():
            valor = q.value(2)
            # valor = qsatype.FLUtil.quickSqlSelect("gt_timetracking", "SUM(totaltiempo)", "idusuario = " + usuario + " AND idtarea IN (Select idtarea from gt_tareas where codproyecto = '" + q.value(1) + "') ")
            if valor:
                valor = flgesttare_def.iface.seconds_to_time(valor.total_seconds(), all_in_hours=True)
                valor = flgesttare_def.iface.time_to_hours(str(valor))
            else:
                valor = 0
            if i > 8:
                otros += valor
            else:
                porcentaje = 0
                if total != 0 and total != None:
                    porcentaje = 100*(valor/total)
                data.append({"name": q.value(0), "value": porcentaje})
            i = i+1
            if i == q.size() and otros > 0:
                if total != 0 and total != None:
                    porcentaje = 100*(otros/total)
                data.append({"name": "Otros Proyectos", "value": porcentaje})

        return {"type": "pieChart", "data": data, "innerText": False}

    def gesttare_cajasinfo(self, oParam):
        horasStyle = {
            "border": "1px solid #dfdfdf",
            "backgroundColor": "white",
            "color": "grey"
        }

        presupuestoStyle = {
            "backgroundColor": "#bababa",
            "color": "#ffffff"
        }

        rentabilidadStyle = {
            "backgroundImage": "linear-gradient(to right, #e79b21, #ffc68d)",
            "color": "#ffffff"
        }


        where = "1=1"
        usuario = qsatype.FLUtil.nameUser()

        locale.setlocale(locale.LC_ALL, '')
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

        where += " AND tt.idusuario = {}".format(usuario)
        tiempo = qsatype.FLUtil.sqlSelect("gt_timetracking tt", "SUM(tt.totaltiempo)", where)

        totalPresupuesto = 0
        totalCostes = 0
        rentabilidad = 0

        #q = qsatype.FLSqlQuery()
        #q.setTablesList("gt_proyectos, gt_particproyecto, aqn_user, gt_tareas, gt_timetracking")
        #q.setSelect("DISTINCT(t.presupuesto), t.costetotal")
        #q.setFrom("gt_proyectos t LEFT JOIN gt_particproyecto p ON t.codproyecto=p.codproyecto INNER JOIN aqn_user u ON u.idusuario = p.idusuario INNER JOIN gt_tareas ta ON t.codproyecto=ta.codproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea")
        #q.setWhere("{}".format(where))

        q = qsatype.FLSqlQuery()
        q.setTablesList("gt_proyectos, gt_tareas, gt_timetracking")
        q.setSelect("t.presupuesto, t.costetotal")
        q.setFrom("gt_proyectos t INNER JOIN gt_tareas ta ON t.codproyecto=ta.codproyecto INNER JOIN gt_timetracking tt ON ta.idtarea=tt.idtarea")
        q.setWhere("{} GROUP BY t.codproyecto".format(where))

        if not q.exec_():
            return []
        if q.size() > 100:
            return []

        #while q.next():
        #    presupuesto = q.value(0)
        #    coste = q.value(1)
        #    totalPresupuesto += presupuesto
        #    totalCostes += coste

        while q.next():
            totalPresupuesto += q.value(0)
            totalCostes += q.value(1)

        if totalPresupuesto != None and totalPresupuesto != 0 and totalCostes != None:
            rentabilidad = ((totalPresupuesto-totalCostes)*100) / totalPresupuesto

        #totalPresupuesto = qsatype.FLUtil.roundFieldValue(totalPresupuesto, "gt_proyectos", "presupuesto")
        totalPresupuesto=(locale.format('%.2f', totalPresupuesto, grouping=True, monetary=True))
        totalPresupuesto = str(totalPresupuesto) +" €"

        rentabilidad = (locale.format('%.2f', rentabilidad, grouping=True))

        if tiempo == None:
            tiempo = "00:00:00"
        else:
            tiempo = flgesttare_def.iface.seconds_to_time(tiempo.total_seconds(), all_in_hours=True)

        data = [{"name": "Horas Invertidas", "value": tiempo, "style": horasStyle} , {"name": "Presupuesto", "value": totalPresupuesto, "style": presupuestoStyle}, {"name": "Rentabilidad", "value": rentabilidad, "style" :rentabilidadStyle}]
        return {"type": "labelInfo", "data": data}

    def gesttare_queryGrid_pruebagrafico(self, model, filters):

        where = "1=1"
        usuario = qsatype.FLUtil.nameUser()
        print("los filtros son: ",filters)

        if not filters:
            hoy = date.today()
            ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
            where += " AND tt.fecha BETWEEN '" + str(hoy.year) + "-" + str(hoy.month) + "-1' AND '" + str(hoy.year) + "-" + str(hoy.month) + "-" + str(ultimo) +"'"
        if filters:
            if "[idusuario]" in filters and filters["[idusuario]"] != "":
                usuario ="'{}'".format(filters["[idusuario]"])
            if "[d_fecha]" in filters and filters["[d_fecha]"]=="" and "[h_fecha]" in filters and filters["[h_fecha]"]=="" and "[fecha]" in filters and filters["[fecha]"]=="":
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
        query["from"] = ("aqn_user a INNER JOIN gt_particproyecto pp ON a.idusuario = pp.idusuario INNER JOIN gt_proyectos p ON pp.codproyecto = p.codproyecto INNER JOIN gt_tareas t ON p.codproyecto = t.codproyecto INNER JOIN gt_timetracking tt ON t.idtarea = tt.idtarea")
        query["where"] = "{} AND tt.totaltiempo < (SELECT MAX(tt.totaltiempo) FROM gt_timetracking tt)".format(where)
        query["orderby"] = (" tt.totaltiempo DESC")

        return query


    def gesttare_calculaGraficosAnalisis(self, oParam):
        response = []
        cajasinfo = self.iface.cajasinfo(oParam)
        response.append(cajasinfo)
        proyectosportiempo = self.iface.graficoproyectosportiempo(oParam)
        response.append(proyectosportiempo)
        #tareasporestado = self.iface.graficostareasporestado(oParam)
        #response.append(tareasporestado)
        horasporproyecto = self.iface.graficohorasporproyecto(oParam)
        response.append(horasporproyecto)
        return response

    def gesttare_generaAnalisisGraphic(self, model, template):
        return self.iface.calculaGraficosAnalisis({})

    def gesttare_getAnalisisGraphic(self, oParam):
        return self.iface.calculaGraficosAnalisis(oParam)


    def __init__(self, context=None):
        super().__init__(context)

    def checkDrawUser(self, cursor):
        return self.ctx.gesttare_checkDrawUser(cursor)

    def checkCambiaPassword(self, cursor):
        return self.ctx.gesttare_checkCambiaPassword(cursor)

    def getUsuariosProyecto(self, oParam):
        return self.ctx.gesttare_getUsuariosProyecto(oParam)

    def getParticipantesProyecto(self, oParam):
        return self.ctx.gesttare_getParticipantesProyecto(oParam)

    def getParticProyectosUsu(self, oParam):
        return self.ctx.gesttare_getParticProyectosUsu(oParam)

    def getParticCompaniaUsu(self, oParam):
        return self.ctx.gesttare_getParticCompaniaUsu(oParam)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def desactivar_usuario(self, model, oParam, cursor):
        return self.ctx.gesttare_desactivar_usuario(model, oParam, cursor)

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

    def cajasinfo(self, oParam):
        return self.ctx.gesttare_cajasinfo(oParam)

    def queryGrid_pruebagrafico(self, model, filters):
        return self.ctx.gesttare_queryGrid_pruebagrafico(model, filters)

