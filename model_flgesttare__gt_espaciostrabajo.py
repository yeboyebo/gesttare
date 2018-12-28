# @class_declaration interna_gt_espaciostrabajo #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_espaciostrabajo(modelos.mtd_gt_espaciostrabajo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_espaciostrabajo #
class gesttare_gt_espaciostrabajo(interna_gt_espaciostrabajo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gt_espaciostrabajo #
class gt_espaciostrabajo(gesttare_gt_espaciostrabajo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_espaciostrabajo_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
