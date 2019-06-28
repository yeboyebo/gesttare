# @class_declaration interna_aqn_invitations #
import importlib

from YBUTILS.viewREST import helpers

from models.fllogin import models as modelos


class interna_aqn_invitations(modelos.mtd_aqn_invitations, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_aqn_invitations #
class gesttare_aqn_invitations(interna_aqn_invitations, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration aqn_invitations #
class aqn_invitations(gesttare_aqn_invitations, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.fllogin.aqn_invitations_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
