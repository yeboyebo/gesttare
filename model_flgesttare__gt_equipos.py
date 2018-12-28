# @class_declaration interna_gt_equipos #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_equipos(modelos.mtd_gt_equipos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_equipos #
class gesttare_gt_equipos(interna_gt_equipos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gt_equipos #
class gt_equipos(gesttare_gt_equipos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_equipos_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
