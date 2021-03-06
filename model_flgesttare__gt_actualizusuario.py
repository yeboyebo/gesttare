# @class_declaration interna_gt_actualizusuario #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_actualizusuario(modelos.mtd_gt_actualizusuario, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_actualizusuario #
class gesttare_gt_actualizusuario(interna_gt_actualizusuario, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gt_actualizusuario #
class gt_actualizusuario(gesttare_gt_actualizusuario, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_actualizusuario_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
