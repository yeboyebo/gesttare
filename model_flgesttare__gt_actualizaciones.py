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

    def queryGrid_notificacionesUsuarioViejas(model):
        return form.iface.queryGrid_notificacionesUsuarioViejas(model)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def visualizarElemento(self, cursor):
        return form.iface.visualizarElemento(self, cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def borrarActualizacion(self, oParam):
        return form.iface.borrarActualizacion(self, oParam)

    def field_nombreUsuario(self):
        return form.iface.field_nombreUsuario(self)

    def field_verConvertirTarea(self):
        return form.iface.field_verConvertirTarea(self)

    def field_verTranspasarAnotacion(self):
        return form.iface.field_verTranspasarAnotacion(self)

    def field_actIcon(self):
        return form.iface.field_actIcon(self)

    def field_color_responsable(self):
        return form.iface.field_color_responsable(self)

    def field_color_fondo_icono(self):
        return form.iface.field_color_fondo_icono(self)

    def field_titulo_icono(self):
        return form.iface.gesttare_field_titulo_icono(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def convertirTarea(self, oParam):
        return form.iface.convertirTarea(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def transpasarAnotacion(self, oParam):
        return form.iface.transpasarAnotacion(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def aceptarColaborador(self, oParam, cursor):
        return form.iface.aceptarColaborador(oParam, cursor)

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
