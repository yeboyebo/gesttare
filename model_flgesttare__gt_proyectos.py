# @class_declaration interna_gt_proyectos #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_proyectos(modelos.mtd_gt_proyectos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_proyectos #
class gesttare_gt_proyectos(interna_gt_proyectos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def actNuevoPartic(self, oParam, cursor):
        return form.iface.actNuevoPartic(oParam, cursor)


# @class_declaration gt_proyectos #
class gt_proyectos(gesttare_gt_proyectos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_proyectos_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
