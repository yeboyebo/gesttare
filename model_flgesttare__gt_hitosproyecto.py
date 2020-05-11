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

    def func_color_hito(self):
        return form.iface.func_color_hito(self)

    def func_presupuesto_title(self):
        return form.iface.func_presupuesto_title(self)
        
    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getHitosProyecto(self, oParam):
        return form.iface.getHitosProyecto(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getHitosProyectosUsu(self, oParam):
        return form.iface.getHitosProyectosUsu(oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def completar_hito(self, oParam, cursor):
        return form.iface.completar_hito(self, oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def creartareahito(self, oParam, cursor):
        return form.iface.creartareahito(oParam, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def abrir_hito(self, cursor):
        return form.iface.abrir_hito(self, cursor)

    def drawif_completarHito(cursor):
        return form.iface.drawif_completarHito(cursor)

    def drawif_abrirHito(cursor):
        return form.iface.drawif_abrirHito(cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def borrar_hito(self, oParam, cursor):
        return form.iface.borrar_hito(self, oParam, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def verTarea(self, cursor):
        return form.iface.verTarea(self, cursor)

    def validateCursor(self):
        return form.iface.validateCursor(self)


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
