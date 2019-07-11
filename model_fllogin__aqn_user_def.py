
# @class_declaration gesttare #
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
        print(data)
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

