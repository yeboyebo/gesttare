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

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def archivar_proyecto(self, oParam, cursor):
        return form.iface.archivar_proyecto(oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def borrar_proyecto(self, oParam, cursor):
        return form.iface.borrar_proyecto(oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def actInvitarExterno(self, oParam, cursor):
        return form.iface.actInvitarExterno(oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def actInvitarExternoColaborador(self, oParam, cursor):
        return form.iface.actInvitarExternoColaborador(oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def actInvitarExternoObservador(self, oParam, cursor):
        return form.iface.actInvitarExternoObservador(oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def invExterno(self, oParam, cursor):
        return form.iface.invExterno(oParam, cursor)

    def field_nombreCliente(self):
        return form.iface.field_nombreCliente(self)

    def field_queryNombreCliente(self):
        return form.iface.field_queryNombreCliente(self)

    def checkProyectosFormDraw(cursor):
        return form.iface.checkProyectosFormDraw(cursor)

    def checkResponsableDraw(cursor):
        return form.iface.checkResponsableDraw(cursor)

    def checkDrawPorcentajeHito(cursor):
        return form.iface.checkDrawPorcentajeHito(cursor)

    def checkProyectosExterno(cursor):
        return form.iface.checkProyectosExterno(cursor)

    def commonCalculateField(fN, curP):
        return form.iface.commonCalculateField(fN, curP)

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    def getRentabilidadGraphic(self, model, template):
        return form.iface.getRentabilidadGraphic(model, template)

    def field_usuario(self):
        return form.iface.field_usuario(self)

    def color_nombre(self):
        return form.iface.color_nombre(self)

    def color_responsable(self):
        return form.iface.color_responsable(self)

    def color_fondo_estado(self):
        return form.iface.color_fondo_estado(self)

    def color_fondo_estado_query(self):
        return form.iface.color_fondo_estado_query(self)

    def color_fondo_resultado(self):
        return form.iface.color_fondo_resultado(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_proyectosarchivados(model, filters):
        return form.iface.queryGrid_proyectosarchivados(model, filters)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_rentabilidadProyectos(model, filters):
        return form.iface.queryGrid_rentabilidadProyectos(model, filters)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def vertareasproyecto(self, cursor):
        return form.iface.vertareasproyecto(cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def verTrackingProyecto(self, cursor):
        return form.iface.verTrackingProyecto(cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def gotoNuevoProyecto(self, oParam):
        return form.iface.gotoNuevoProyecto(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def copiarProyecto(self, oParam, cursor):
        return form.iface.copiarProyecto(oParam, cursor)

    def copiarTareasProyecto(self, cursor, idproyecto, idhito):
        return form.iface.copiarTareasProyecto(cursor, idproyecto, idhito)

    def copiarHitosProyecto(self, cursor, idproyecto):
        return form.iface.copiarHitosProyecto(cursor, idproyecto)

    def validateCursor(self):
        return form.iface.validateCursor(self)

    @helpers.decoradores.accion()
    def gotoProyecto(self):
        return form.iface.gotoProyecto(self)

    def drawif_archivado(cursor):
        return form.iface.drawif_archivado(cursor)


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
