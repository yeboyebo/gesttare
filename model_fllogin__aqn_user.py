# @class_declaration interna_aqn_user #
import importlib

from YBUTILS.viewREST import helpers

from models.fllogin import models as modelos


class interna_aqn_user(modelos.mtd_aqn_user, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_aqn_user #
class gesttare_aqn_user(interna_aqn_user, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration aqn_user #
class aqn_user(gesttare_aqn_user, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.fllogin.aqn_user_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
