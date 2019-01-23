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
        fields = [
            {'verbose_name': 'Hora inicio', 'func': 'field_inicioformateado'},
            {'verbose_name': 'Hora fin', 'func': 'field_finformateado'},
            {'verbose_name': 'Total tiempo', 'func': 'field_totalformateado'},
            {'verbose_name': 'Usuario', 'func': 'field_usuario'},
            {'verbose_name': 'Tarea', 'func': 'field_tarea'},
            {'verbose_name': 'Proyecto', 'func': 'field_proyecto'}
        ]
        return fields

    def gesttare_field_inicioformateado(self, model):
        return self.seconds_to_time(model.horainicio)

    def gesttare_field_finformateado(self, model):
        return self.seconds_to_time(model.horafin)

    def gesttare_field_totalformateado(self, model):
        return self.seconds_to_time(model.totaltiempo)

    def gesttare_field_usuario(self, model):
        return model.idusuario.nombre

    def gesttare_field_tarea(self, model):
        return model.idtarea.nombre

    def gesttare_field_proyecto(self, model):
        # Si sacamos el proyecto de la tarea
        # if model.idtarea.codproyecto:
        #     return model.idtarea.codproyecto.codproyecto
        # return ""
        if model.codproyecto:
            return model.codproyecto.codproyecto
        return ""

    def gesttare_seconds_to_time(self, seconds):
        if not seconds:
            return ""

        minutes = seconds // 60
        seconds = int(seconds % 60)
        hours = minutes // 60
        minutes = int(minutes % 60)
        hours = int(hours % 24)

        seconds = str(seconds) if seconds >= 10 else "0{}".format(seconds)
        minutes = str(minutes) if minutes >= 10 else "0{}".format(minutes)
        hours = str(hours) if hours >= 10 else "0{}".format(hours)

        return "{}:{}:{}".format(hours, minutes, seconds)

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def field_inicioformateado(self, model):
        return self.ctx.gesttare_field_inicioformateado(model)

    def field_finformateado(self, model):
        return self.ctx.gesttare_field_finformateado(model)

    def field_totalformateado(self, model):
        return self.ctx.gesttare_field_totalformateado(model)

    def field_usuario(self, model):
        return self.ctx.gesttare_field_usuario(model)

    def field_tarea(self, model):
        return self.ctx.gesttare_field_tarea(model)

    def field_proyecto(self, model):
        return self.ctx.gesttare_field_proyecto(model)

    def seconds_to_time(self, seconds):
        return self.ctx.gesttare_seconds_to_time(seconds)


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
