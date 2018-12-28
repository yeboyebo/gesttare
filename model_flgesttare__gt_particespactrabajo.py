# @class_declaration interna_gt_particespactrabajo #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_particespactrabajo(modelos.mtd_gt_particespactrabajo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_particespactrabajo #
class gesttare_gt_particespactrabajo(interna_gt_particespactrabajo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gt_particespactrabajo #
class gt_particespactrabajo(gesttare_gt_particespactrabajo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_particespactrabajo_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
