# @class_declaration interna_aqn_modules #
import importlib

from YBUTILS.viewREST import helpers

from models.fllogin import models as modelos


class interna_aqn_modules(modelos.mtd_aqn_modules, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_aqn_modules #
class gesttare_aqn_modules(interna_aqn_modules, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration aqn_modules #
class aqn_modules(gesttare_aqn_modules, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.fllogin.aqn_modules_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
