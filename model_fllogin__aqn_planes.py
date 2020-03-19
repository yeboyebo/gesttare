# @class_declaration interna_aqn_planes #
import importlib

from YBUTILS.viewREST import helpers

from models.fllogin import models as modelos


class interna_aqn_planes(modelos.mtd_aqn_planes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_aqn_planes #
class gesttare_aqn_planes(interna_aqn_planes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration aqn_planes #
class aqn_planes(gesttare_aqn_planes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.fllogin.aqn_planes_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
