# @class_declaration interna_gt_timetracking #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_timetracking(modelos.mtd_gt_timetracking, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_timetracking #
class gesttare_gt_timetracking(interna_gt_timetracking, helpers.MixinConAcciones):
    pass

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_mastertimetracking(model, filters):
        return form.iface.queryGrid_mastertimetracking(model, filters)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def editartt(self, oParam, cursor):
        return form.iface.editarTT(oParam, cursor)

    class Meta:
        proxy = True


# @class_declaration gt_timetracking #
class gt_timetracking(gesttare_gt_timetracking, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_timetracking_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
