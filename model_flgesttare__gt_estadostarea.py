# @class_declaration interna_gt_estadostarea #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_estadostarea(modelos.mtd_gt_estadostarea, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_estadostarea #
class gesttare_gt_estadostarea(interna_gt_estadostarea, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gt_estadostarea #
class gt_estadostarea(gesttare_gt_estadostarea, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_estadostarea_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
