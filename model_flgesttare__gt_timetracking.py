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

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_mastertimetrackingagrupado(model, filters):
        return form.iface.queryGrid_mastertimetrackingagrupado(model, filters)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def editartt(self, oParam, cursor):
        return form.iface.editarTT(oParam, cursor)

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    def bChCursor(fN, cursor):
        return form.iface.bChCursor(fN, cursor)

    def field_nombre(self):
        return form.iface.field_nombre(self)

    def color_usuario(self):
        return form.iface.color_usuario(self)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def verTarea(self, cursor):
        return form.iface.verTarea(self, cursor)

    def checkTimeTrackingDraw(cursor):
        return form.iface.checkTimeTrackingDraw(cursor)

    def field_proyecto(self):
        return form.iface.field_proyecto(self)

    def field_sumTotalTiempo(self):
        return form.iface.field_sumTotalTiempo(self)

    def field_cliente(self):
        return form.iface.field_cliente(self)

    @helpers.decoradores.accion(aqparam=[])
    def set_estado_agrupado(self):
        return form.iface.set_estado("agrupado")

    @helpers.decoradores.accion(aqparam=[])
    def set_estado_noagrupado(self):
        return form.iface.set_estado("noagrupado")

    def drawif_noagrupado(cursor):
        return form.iface.drawif_noagrupado(cursor)

    def drawif_agrupado(cursor):
        return form.iface.drawif_agrupado(cursor)

    def drawif_botonnoagrupado(cursor):
        return form.iface.drawif_botonnoagrupado(cursor)

    def drawif_botonagrupado(cursor):
        return form.iface.drawif_botonagrupado(cursor)

    def color_nombreProyecto(self):
        return form.iface.color_nombreProyecto(self)

    def color_nombreProyectoT(self):
        return form.iface.color_nombreProyectoT(self)

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
