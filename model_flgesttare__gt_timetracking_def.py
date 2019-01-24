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

    def gesttare_get_model_info(self, model, data, ident, template, where_filter):
        if template == "mastertimetracking":
            if not where_filter:
                where_filter = "1 = 1"

            tiempototal = qsatype.FLUtil.quickSqlSelect("gt_timetracking INNER JOIN gt_tareas ON gt_timetracking.idtarea = gt_tareas.idtarea LEFT OUTER JOIN gt_proyectos ON gt_tareas.codproyecto = gt_proyectos.codproyecto INNER JOIN usuarios ON gt_timetracking.idusuario = usuarios.idusuario", "SUM(totaltiempo)", where_filter)

            return {"masterTimeTracking": "Tiempo total: {}".format(self.seconds_to_time(tiempototal, total=True))}
        return None

    def gesttare_queryGrid_mastertimetracking(self, model):
        query = {}
        query["tablesList"] = ("gt_timetracking, gt_tareas, usuarios")
        query["select"] = ("gt_timetracking.idtracking, gt_timetracking.fecha, gt_timetracking.horainicio, gt_timetracking.horafin, gt_timetracking.totaltiempo, gt_tareas.nombre, gt_proyectos.codproyecto, usuarios.nombre")
        query["from"] = ("gt_timetracking INNER JOIN gt_tareas ON gt_timetracking.idtarea = gt_tareas.idtarea LEFT OUTER JOIN gt_proyectos ON gt_tareas.codproyecto = gt_proyectos.codproyecto INNER JOIN usuarios ON gt_timetracking.idusuario = usuarios.idusuario")
        query["where"] = ("1 = 1")
        query["orderby"] = ("gt_timetracking.fecha DESC, gt_timetracking.horainicio DESC")
        return query

    def gesttare_getForeignFields(self, model, template=None):
        if template == "mastertimetracking":
            return [
                {'verbose_name': 'Hora inicio', 'func': 'field_inicioformateado'},
                {'verbose_name': 'Hora fin', 'func': 'field_finformateado'},
                {'verbose_name': 'Total tiempo', 'func': 'field_totalformateado'}
            ]
        return []

    def gesttare_field_inicioformateado(self, model):
        return self.seconds_to_time(model["gt_timetracking.horainicio"])

    def gesttare_field_finformateado(self, model):
        return self.seconds_to_time(model["gt_timetracking.horafin"])

    def gesttare_field_totalformateado(self, model):
        return self.seconds_to_time(model["gt_timetracking.totaltiempo"])

    def gesttare_seconds_to_time(self, seconds, total=False):
        if not seconds:
            seconds = 0

        minutes = seconds // 60
        seconds = int(seconds % 60)
        hours = minutes // 60
        minutes = int(minutes % 60)

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

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def get_model_info(self, model, data, ident, template, where_filter):
        return self.ctx.gesttare_get_model_info(model, data, ident, template, where_filter)

    def queryGrid_mastertimetracking(self, model):
        return self.ctx.gesttare_queryGrid_mastertimetracking(model)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def field_inicioformateado(self, model):
        return self.ctx.gesttare_field_inicioformateado(model)

    def field_finformateado(self, model):
        return self.ctx.gesttare_field_finformateado(model)

    def field_totalformateado(self, model):
        return self.ctx.gesttare_field_totalformateado(model)

    def seconds_to_time(self, seconds, total=False):
        return self.ctx.gesttare_seconds_to_time(seconds, total)


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
