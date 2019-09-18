# @class_declaration interna_gt_clientes #
import importlib

from YBUTILS.viewREST import helpers

from models.flgesttare import models as modelos


class interna_gt_clientes(modelos.mtd_gt_clientes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_clientes #
class gesttare_gt_clientes(interna_gt_clientes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getClientesCompaniaUsu(self, oParam):
        return form.iface.getClientesCompaniaUsu(oParam)


# @class_declaration gt_clientes #
class gt_clientes(gesttare_gt_clientes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_clientes_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
