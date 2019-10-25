# @class_declaration interna_gt_actualizaciones #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_actualizaciones(modelos.mtd_gt_actualizaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_actualizaciones #
class gesttare_gt_actualizaciones(interna_gt_actualizaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def queryGrid_notificacionesUsuario(model):
        return form.iface.queryGrid_notificacionesUsuario(model)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def visualizarElemento(self, cursor):
        return form.iface.visualizarElemento(self, cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def borrarActualizacion(self, oParam):
        return form.iface.borrarActualizacion(self, oParam)

    def field_nombreUsuario(self):
        return form.iface.field_nombreUsuario(self)


# @class_declaration gt_actualizaciones #
class gt_actualizaciones(gesttare_gt_actualizaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_actualizaciones_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
