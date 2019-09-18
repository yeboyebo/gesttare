# @class_declaration interna_gesttare_clients #
import importlib

from YBUTILS.viewREST import helpers

from models.fllogin import models as modelos


class interna_gesttare_clients(modelos.mtd_gesttare_clients, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gesttare_clients #
class gesttare_gesttare_clients(interna_gesttare_clients, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_clients #
class gesttare_clients(gesttare_gesttare_clients, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.fllogin.gesttare_clients_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
