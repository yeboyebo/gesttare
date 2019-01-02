# @class_declaration interna_gt_listatareas #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_listatareas(modelos.mtd_gt_listatareas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_listatareas #
class gesttare_gt_listatareas(interna_gt_listatareas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gt_listatareas #
class gt_listatareas(gesttare_gt_listatareas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_listatareas_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
