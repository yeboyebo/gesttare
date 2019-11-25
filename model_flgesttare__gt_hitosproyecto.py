# @class_declaration interna_gt_hitosproyecto #
import importlib

from YBUTILS.viewREST import helpers

from models.flgesttare import models as modelos


class interna_gt_hitosproyecto(modelos.mtd_gt_hitosproyecto, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_hitosproyecto #
class gesttare_gt_hitosproyecto(interna_gt_hitosproyecto, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_usuario(self):
        return form.iface.field_usuario(self)
        
    def color_responsable(self):
        return form.iface.color_responsable(self)

    def fun_porcentaje(self):
        return form.iface.fun_porcentaje(self)

    def fun_ntareas(self):
        return form.iface.fun_ntareas(self)
        
    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getHitosProyecto(self, oParam):
        return form.iface.getHitosProyecto(oParam)


# @class_declaration gt_hitosproyecto #
class gt_hitosproyecto(gesttare_gt_hitosproyecto, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_hitosproyecto_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
