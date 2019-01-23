# @class_declaration interna_gt_timetracking #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_timetracking(modelos.mtd_gt_timetracking, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_timetracking #
class gesttare_gt_timetracking(interna_gt_timetracking, helpers.MixinConAcciones):
    pass

    def field_inicioformateado(self):
        return form.iface.field_inicioformateado(self)

    def field_finformateado(self):
        return form.iface.field_finformateado(self)

    def field_totalformateado(self):
        return form.iface.field_totalformateado(self)

    def field_usuario(self):
        return form.iface.field_usuario(self)

    def field_tarea(self):
        return form.iface.field_tarea(self)

    def field_proyecto(self):
        return form.iface.field_proyecto(self)

    class Meta:
        proxy = True


# @class_declaration gt_timetracking #
class gt_timetracking(gesttare_gt_timetracking, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_timetracking_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
