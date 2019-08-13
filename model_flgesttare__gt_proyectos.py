# @class_declaration interna_gt_proyectos #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_proyectos(modelos.mtd_gt_proyectos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_proyectos #
class gesttare_gt_proyectos(interna_gt_proyectos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def actNuevoPartic(self, oParam, cursor):
        return form.iface.actNuevoPartic(oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getProyectosUsuario(self, oParam):
        return form.iface.getProyectosUsuario(oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def dameEmailCreaTarea(self, oParam, cursor):
        return form.iface.dameEmailCreaTarea(oParam, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def borrar_proyecto(self, cursor):
        return form.iface.borrar_proyecto(cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def actInvitarExterno(self, oParam, cursor):
        return form.iface.actInvitarExterno(oParam, cursor)

    def checkProyectosFormDraw(cursor):
        return form.iface.checkProyectosFormDraw(cursor)

    def checkResponsableDraw(cursor):
        return form.iface.checkResponsableDraw(cursor)

    def commonCalculateField(fN, curP):
        return form.iface.commonCalculateField(fN, curP)

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    def getRentabilidadGraphic(self, template):
        return form.iface.getRentabilidadGraphic(template)

# @class_declaration gt_proyectos #
class gt_proyectos(gesttare_gt_proyectos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_proyectos_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
