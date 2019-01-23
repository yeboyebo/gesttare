# @class_declaration interna #
from YBLEGACY import qsatype
from YBUTILS import gesDoc

from models.flfactppal.usuarios import usuarios

import hashlib


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *


class gesttare(interna):

    def gesttare_fun_totalDays(self, model):
        return 30

    def gesttare_getForeignFields(self, model, template=None):
        fields = [
            {'verbose_name': 'Proyecto', 'func': 'field_proyecto'},
            {'verbose_name': 'Activa', 'func': 'field_activa'}
        ]

        if template == "calendarioTareas":
            return [{'verbose_name': 'totalDays', 'func': 'fun_totalDays'}]

        return fields

    def gesttare_getDesc(self):
        return None

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
        initFilter['where'] = u" AND extract(year from gt_tareas.fechavencimiento) = 2019"
        initFilter['where'] += u" AND extract(month from gt_tareas.fechavencimiento) = " + str(qsatype.Date().getMonth())
        initFilter['filter'] = {"s_extract(year from gt_tareas.fechavencimiento)__exact": "2019", "s_extract(month from gt_tareas.fechavencimiento)__exact": str(qsatype.Date().getMonth())}
        return initFilter

    def gesttare_queryGrid_calendarioTareas(self, model):
        query = {}
        query["tablesList"] = ("gt_tareas")
        query["select"] = ("gt_tareas.idtarea, gt_tareas.codproyecto, gt_tareas.codestado, gt_tareas.codespacio, gt_tareas.idusuario, gt_tareas.fechavencimiento, gt_tareas.nombre, extract(day from gt_tareas.fechavencimiento) as day, extract(month from gt_tareas.fechavencimiento) as month, extract(year from gt_tareas.fechavencimiento) as year, extract(dow from date_trunc('month', gt_tareas.fechavencimiento)) as firstDay")
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
        try:
            if not model.codproyecto:
                return nombreProy
            nombreProy = model.codproyecto.nombre
        except Exception:
            pass
        return nombreProy

    def gesttare_field_activa(self, model):
        return model.idtarea == qsatype.FLUtil.quickSqlSelect("usuarios", "idtareaactiva", "idusuario = '{}'".format(qsatype.FLUtil.nameUser()))

    def gesttare_uploadFile(self, model, oParam):
        # print(u"gt_comentarios", [u"idtarea", u"fecha", u"hora", u"comentario", u"idusuario"], [model.idtarea, str(qsatype.Date())[:10], str(qsatype.Date())[-8:], oParam['comentario'], 1])
        # TODO De donde sacamos idusuario, al crear usuario en aplicacion acreamos gt_usuario?
        nombreUsuario = qsatype.FLUtil.nameUser()
        idUsuario = qsatype.FLUtil.sqlSelect(u"usuarios", u"idusuario", ustr(u"idusuario = '", nombreUsuario, u"'"))
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
        if not gesDoc.fileUpload("gt_comentarios", cursor.valueBuffer("idcomentario"), oParam['FILES']):
            return False
        return True

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

    def gesttare_damepryus(self, oParam):
        _i = self.iface
        data = []
        if oParam["appid"] == "23553220-e1b3-4592-a5de-fb41a08c60c8":
            proyectos = _i.dameProyectos()
            usuarios = _i.dameUsuarios()
            data.append({"projects": proyectos})
            data.append({"users": usuarios})
        else:
            data.append({"result": False})
            data.append({"error": "Error en autenticación"})

        return data

    def gesttare_dameProyectos(self):
        proyectos = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_proyectos")
        q.setSelect("codproyecto, descripcion")
        q.setFrom("gt_proyectos")

        if not q.exec_():
            print("Error inesperado")
            return []

        while q.next():
            proyectos.append({"codigo": str(q.value(0)), "descripcion": str(q.value(1))})

        return proyectos

    def gesttare_dameUsuarios(self):
        usuarios = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_usuarios")
        q.setSelect("iduser, nombre")
        q.setFrom("gt_usuarios")

        if not q.exec_():
            print("Error inesperado")
            return []

        while q.next():
            usuarios.append({"codigo": str(q.value(0)), "nombre": str(q.value(1))})

        return usuarios

    def gesttare_calcula_totaltiempo(self, cursor):
        return cursor.valueBuffer("horafin") - cursor.valueBuffer("horainicio")

    def gesttare_startstop(self, model, cursor):
        now = qsatype.Date()
        user_name = qsatype.FLUtil.nameUser()

        cur_track = qsatype.FLSqlCursor("gt_timetracking")

        cur_user = qsatype.FLSqlCursor("usuarios")
        cur_user.select("idusuario = '{}'".format(user_name))
        if not cur_user.first():
            print("No se encontró el usuario")
            return False

        cur_user.setModeAccess(cur_user.Edit)
        cur_user.refreshBuffer()

        if self.field_activa(model):
            cur_track.select("idusuario = '{}' AND idtarea = {} AND horafin IS NULL".format(user_name, cursor.valueBuffer("idtarea")))

            if not cur_track.first():
                print("No se encontró el registro de timetracking")
                return False

            cur_track.setModeAccess(cur_track.Edit)
            cur_track.refreshBuffer()

            cur_track.setValueBuffer("horafin", int(now.getTime() / 1000))
            cur_track.setValueBuffer("totaltiempo", self.calcula_totaltiempo(cur_track))

            cur_user.setNull("idtareaactiva")
        else:
            if not cur_user.isNull("idtareaactiva"):
                print("Ya existe una tarea activa")
                return False

            cur_track.setModeAccess(cur_track.Insert)
            cur_track.refreshBuffer()

            cur_track.setValueBuffer("fecha", now.toString()[:10])
            cur_track.setValueBuffer("horainicio", int(now.getTime() / 1000))
            cur_track.setValueBuffer("idusuario", user_name)
            cur_track.setValueBuffer("idtarea", cursor.valueBuffer("idtarea"))
            cur_track.setValueBuffer("codproyecto", cursor.valueBuffer("codproyecto"))

            cur_user.setValueBuffer("idtareaactiva", cursor.valueBuffer("idtarea"))

        if not cur_track.commitBuffer():
            print("Ocurrió un error al guardar el registro de gt_timetracking")
            return False
        if not cur_user.commitBuffer():
            print("Ocurrió un error al actualizar la tarea activa")
            return False

        return True

    def gesttare_creartarea(self, oParam):
        data = []
        usuario = usuarios.objects.filter(idusuario__exact=oParam["person"])
        if len(usuario) == 0:
            data.append({"result": False})
            data.append({"error": "No existe el usuario"})
            return data
        if oParam["appid"] == "23553220-e1b3-4592-a5de-fb41a08c60c8":
            curTarea = qsatype.FLSqlCursor(u"gt_tareas")
            curTarea.setModeAccess(curTarea.Insert)
            curTarea.refreshBuffer()
            curTarea.setActivatedBufferCommited(True)
            curTarea.setValueBuffer(u"codproyecto", oParam["project"])
            curTarea.setValueBuffer(u"codestado", oParam["state"])
            curTarea.setValueBuffer(u"nombre", oParam["name"])
            curTarea.setValueBuffer(u"idusuario", oParam["person"])
            curTarea.setValueBuffer(u"descripcion", oParam["description"])
            if oParam["date"] and oParam["date"] != u"undefined":
                curTarea.setValueBuffer(u"fechavencimiento", oParam["date"])

            if not curTarea.commitBuffer():
                data.append({"result": False})
                data.append({"error": "Error en commit"})
            else:
                data.append({"result": True})
                data.append({"ok": "Tarea creada correctamente"})
        else:
            data.append({"result": False})
            data.append({"error": "Error en autenticación"})
        return data

    def gesttare_actNuevoPartic(self, oParam, cursor):
        response = {}
        if "partic" not in oParam:
            # idUsuario = cursor.valueBuffer("idusuario")
            qryUsuarios = qsatype.FLSqlQuery()
            qryUsuarios.setTablesList(u"usuarios")
            qryUsuarios.setSelect(u"idusuario, nombre")
            qryUsuarios.setFrom(ustr(u"usuarios"))
            # qryUsuarios.setWhere(ustr(u"idusuario <> '", idUsuario, u"'"))
            qryUsuarios.setWhere(ustr(u"1 = 1"))
            if not qryUsuarios.exec_():
                return False
            opts = []
            while qryUsuarios.next():
                tengousuario = qsatype.FLUtil.sqlSelect(u"gt_partictarea", u"idusuario", ustr(u"idusuario = '", qryUsuarios.value("idusuario"), u"' AND idtarea = '", cursor.valueBuffer("idtarea"), "'"))
                value = False
                if tengousuario:
                    value = True
                opts.append({"key": qryUsuarios.value("idusuario"), "label": qryUsuarios.value("nombre"), "value": value})
            print("_____________")
            print(opts)
            response['status'] = -1
            response['data'] = {}
            response['params'] = [
                {
                    "componente": "YBFieldDB",
                    "prefix": "gt_tareas",
                    "style": {
                        "width": "100%"
                    },
                    "tipo": 180,
                    "verbose_name": "Participantes",
                    "label": "Participantes",
                    "key": "partic",
                    "validaciones": None,
                    "required": False,
                    "opts": opts
                }
            ]
            return response
        else:
            participantes = json.loads(oParam["partic"])
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

            return True

    def __init__(self, context=None):
        super().__init__(context)

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

    def field_activa(self, model):
        return self.ctx.gesttare_field_activa(model)

    def uploadFile(self, model, oParam):
        return self.ctx.gesttare_uploadFile(model, oParam)

    def login(self, oParam):
        return self.ctx.gesttare_login(oParam)

    def damepryus(self, oParam):
        return self.ctx.gesttare_damepryus(oParam)

    def dameProyectos(self):
        return self.ctx.gesttare_dameProyectos()

    def dameUsuarios(self):
        return self.ctx.gesttare_dameUsuarios()

    def startstop(self, model, cursor):
        return self.ctx.gesttare_startstop(model, cursor)

    def calcula_totaltiempo(self, cursor):
        return self.ctx.gesttare_calcula_totaltiempo(cursor)

    def creartarea(self, oParam):
        return self.ctx.gesttare_creartarea(oParam)

    def actNuevoPartic(self, oParam, cursor):
        return self.ctx.gesttare_actNuevoPartic(oParam, cursor)


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
