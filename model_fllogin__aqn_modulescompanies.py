# @class_declaration interna_aqn_modulescompanies #
import importlib

from YBUTILS.viewREST import helpers

from models.fllogin import models as modelos


class interna_aqn_modulescompanies(modelos.mtd_aqn_modulescompanies, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_aqn_modulescompanies #
class gesttare_aqn_modulescompanies(interna_aqn_modulescompanies, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration aqn_modulescompanies #
class aqn_modulescompanies(gesttare_aqn_modulescompanies, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.fllogin.aqn_modulescompanies_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface