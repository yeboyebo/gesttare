# @class_declaration interna_gt_partictarea #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_partictarea(modelos.mtd_gt_partictarea, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_partictarea #
class gesttare_gt_partictarea(interna_gt_partictarea, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def get_model_info(model, data, pag, where_filter):
        return form.iface.get_model_info(model, data, pag, where_filter)

    def field_nombre(self):
        return form.iface.field_nombre(self)

    def color_nombre_participante(self):
        return form.iface.color_nombre_participante(self)


# @class_declaration gt_partictarea #
class gt_partictarea(gesttare_gt_partictarea, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_partictarea_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
