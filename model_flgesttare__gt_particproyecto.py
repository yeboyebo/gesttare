# @class_declaration interna_gt_particproyecto #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_particproyecto(modelos.mtd_gt_particproyecto, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_particproyecto #
class gesttare_gt_particproyecto(interna_gt_particproyecto, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def get_model_info(model, data, pag, where_filter):
        return form.iface.get_model_info(model, data, pag, where_filter)

    def field_nombre(self):
        return form.iface.field_nombre(self)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def borrarPartic(self, oParam, cursor):
        return form.iface.borrarPartic(oParam, cursor)

# @class_declaration gt_particproyecto #
class gt_particproyecto(gesttare_gt_particproyecto, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_particproyecto_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
