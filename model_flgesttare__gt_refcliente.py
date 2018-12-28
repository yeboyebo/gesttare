# @class_declaration interna_gt_refcliente #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_refcliente(modelos.mtd_gt_refcliente, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_refcliente #
class gesttare_gt_refcliente(interna_gt_refcliente, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gt_refcliente #
class gt_refcliente(gesttare_gt_refcliente, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_refcliente_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
