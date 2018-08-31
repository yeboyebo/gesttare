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

    def initValidation(name, data=None):
        return form.iface.initValidation(name, data)

    def iniciaValoresLabel(self, template=None, cursor=None, data=None):
        return form.iface.iniciaValoresLabel(self, template, cursor)

    def bChLabel(fN=None, cursor=None):
        return form.iface.bChLabel(fN, cursor)

    def getFilters(self, name, template=None):
        return form.iface.getFilters(self, name, template)

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def getDesc():
        return form.iface.getDesc()

    def queryGrid_notificacionesUsuario(model):
        return form.iface.queryGrid_notificacionesUsuario(model)

    @helpers.decoradores.accion(miparam=[])
    def visualizarTarea(self):
        return form.iface.visualizarTarea(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def borrarActualizacion(self, oParam):
        print(self)
        return form.iface.borrarActualizacion(self, oParam)


# @class_declaration gt_actualizaciones #
class gt_actualizaciones(gesttare_gt_actualizaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


definitions = importlib.import_module("models.flgesttare.gt_actualizaciones_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
