# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
from datetime import datetime
from models.flgesttare import flgesttare_def


class gesttare(interna):

    def gesttare_getDesc(self):
        return None

    def gesttare_get_model_info(self, model, data, ident, template, where_filter):
        if template == "mastertimetracking":
            if not where_filter:
                where_filter = "1 = 1"
                usuario = qsatype.FLUtil.nameUser()
                curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
                curProyectos.select("idusuario = '" + str(usuario) + "'")
                proin = "("
                while curProyectos.next():
                    curProyectos.setModeAccess(curProyectos.Browse)
                    curProyectos.refreshBuffer()
                    # proin.append(curProyectos.valueBuffer("codproyecto"))
                    proin = proin + "'" + curProyectos.valueBuffer("codproyecto") + "', "
                proin = proin + " null)"
                where_filter += " AND (gt_proyectos.codproyecto IN " + proin + " OR gt_tareas.codproyecto IS NULL)"

            tiempototal = qsatype.FLUtil.quickSqlSelect("gt_timetracking INNER JOIN gt_tareas ON gt_timetracking.idtarea = gt_tareas.idtarea LEFT OUTER JOIN gt_proyectos ON gt_tareas.codproyecto = gt_proyectos.codproyecto INNER JOIN aqn_user ON gt_timetracking.idusuario = aqn_user.idusuario", "SUM(totaltiempo)", where_filter) or 0

            tiempototal = flgesttare_def.iface.seconds_to_time(tiempototal.total_seconds(), all_in_hours=True)
            return {"masterTimeTracking": "Tiempo total: {}".format(tiempototal)}
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
            # proin.append(curProyectos.valueBuffer("codproyecto"))
            proin = proin + "'" + curProyectos.valueBuffer("codproyecto") + "', "
        proin = proin + " null)"
        where += " AND (gt_proyectos.codproyecto IN " + proin + " OR gt_tareas.codproyecto IS NULL)"

        if filters:
            if "[proyecto]" in filters and filters["[proyecto]"] != "":
                where += " AND gt_proyectos.codproyecto = '{}'".format(filters["[proyecto]"])
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
            if "[buscador]" in filters and filters["[buscador]"] != "":
                where += " AND UPPER(gt_proyectos.nombre) LIKE '%" + filters["[buscador]"].upper() + "%' OR UPPER(gt_tareas.nombre) LIKE '%" + filters["[buscador]"].upper() + "%' OR UPPER(aqn_user.nombre) LIKE '%" + filters["[buscador]"].upper() + "%'"

        query = {}
        query["tablesList"] = ("gt_timetracking, gt_tareas, aqn_user")
        query["select"] = ("gt_timetracking.idtracking, gt_timetracking.fecha, gt_timetracking.horainicio, gt_timetracking.horafin, gt_timetracking.totaltiempo, gt_tareas.nombre, gt_proyectos.nombre, aqn_user.usuario, aqn_user.nombre")
        query["from"] = ("gt_timetracking INNER JOIN gt_tareas ON gt_timetracking.idtarea = gt_tareas.idtarea LEFT OUTER JOIN gt_proyectos ON gt_tareas.codproyecto = gt_proyectos.codproyecto INNER JOIN aqn_user ON gt_timetracking.idusuario = aqn_user.idusuario")
        query["where"] = (where)
        query["orderby"] = ("gt_timetracking.fecha DESC, gt_timetracking.horainicio DESC")

        return query

    def gesttare_getForeignFields(self, model, template=None):
        # if template == "mastertimetracking":
            # return [{'verbose_name': 'nombreusuario', 'func': 'field_nombre'}]
        fields = [
            {'verbose_name': 'Color usuario', 'func': 'color_usuario'},
            {'verbose_name': 'aqn_user.usuario', 'func': 'field_nombre'}
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

        if template == "formRecord":
            curTracking = qsatype.FLSqlCursor("gt_timetracking")
            curTracking.select(ustr("idtracking = '", pk, "'"))
            curTracking.refreshBuffer()
            if curTracking.first():
                usuario = qsatype.FLUtil.nameUser()
                curTracking.setModeAccess(curTracking.Browse)
                curTracking.refreshBuffer()
                # idtarea = curTracking.valueBuffer("idtarea")
                # codproyecto = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"codproyecto", ustr(u"idtarea = '", idtarea, u"'"))
                # nombreUsuario = qsatype.FLUtil.nameUser()
                # pertenece = qsatype.FLUtil.sqlSelect(u"gt_particproyecto", u"idusuario", ustr(u"idusuario = '", nombreUsuario, u"' AND codproyecto = '", codproyecto, "'"))
                pertenece = str(curTracking.valueBuffer("idusuario")) == str(usuario)
                print(usuario)
                print(curTracking.valueBuffer("idusuario"))
                if not pertenece:
                    return False
            else:
                return False
        return True

    def gesttare_verTarea(self, model, cursor):
        url = "/gesttare/gt_tareas/" + str(cursor.valueBuffer("idtarea"))
        return url

    def gesttare_color_usuario(self, model):
        # print(model['aqn_user.usuario'])
        # if (model['aqn_user.usuario']):
        #     return "usuario"

        return "usuario"

    def __init__(self, context=None):
        super().__init__(context)

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.gesttare_iniciaValoresCursor(cursor)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def get_model_info(self, model, data, ident, template, where_filter):
        return self.ctx.gesttare_get_model_info(model, data, ident, template, where_filter)

    def queryGrid_mastertimetracking(self, model, filters):
        return self.ctx.gesttare_queryGrid_mastertimetracking(model, filters)

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
