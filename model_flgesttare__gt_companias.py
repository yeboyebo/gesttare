# @class_declaration interna_gt_companias #
import importlib
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos


class interna_gt_companias(modelos.mtd_gt_companias, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_companias #
class gesttare_gt_companias(interna_gt_companias, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gt_companias #
class gt_companias(gesttare_gt_companias, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_companias_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
