# @class_declaration interna_gt_tareas #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_tareas(modelos.mtd_gt_tareas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_tareas #
class gesttare_gt_tareas(interna_gt_tareas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def actNuevoComentario(self, oParam):
        return form.iface.actNuevoComentario(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def actNuevoPartic(self, oParam, cursor):
        return form.iface.actNuevoPartic(oParam, cursor)

    def queryGrid_calendarioTareas(model):
        return form.iface.queryGrid_calendarioTareas(model)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getListaTarea(self, oParam):
        return form.iface.getListaTarea(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def uploadFile(self, oParam):
        return form.iface.uploadFile(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def cambiarFecha(self, oParam, cursor):
        return form.iface.cambiarFecha(self, oParam, cursor)

    def fun_totalDays(self):
        return form.iface.fun_totalDays(self)

    def fun_firstDay(self):
        return form.iface.fun_firstDay(self)

    def queryGrid_calendarioTareas_initFilter(model=None):
        return form.iface.queryGrid_calendarioTareas_initFilter()

    def field_proyecto(self):
        return form.iface.field_proyecto(self)

    def ren_field_proyecto(self):
        return form.iface.ren_field_proyecto(self)

    def field_usuario(self):
        return form.iface.field_usuario(self)

    def color_fecha(self):
        return form.iface.color_fecha(self)

    def color_fechaentrega(self):
        return form.iface.color_fechaentrega(self)

    def ren_color_fecha(self):
        return form.iface.ren_color_fecha(self)

    def ren_color_fechaentrega(self):
        return form.iface.ren_color_fechaentrega(self)

    def color_nombre(self):
        return form.iface.color_nombre(self)

    @helpers.decoradores.csr()
    def login(oParam):
        return form.iface.login(oParam)

    def getpryus(appid, email):
        return form.iface.getpryus(appid, email)

    @helpers.decoradores.csr()
    def damepryus(oParam):
        return form.iface.damepryus(oParam["appid"], oParam["email"])

    @helpers.decoradores.csr()
    def creartarea(oParam):
        return form.iface.creartarea(oParam)

    def createtask(oParam):
        return form.iface.createtask(oParam)

    def dameProyectos(email):
        return form.iface.dameProyectos(email)

    def dameUsuarios(email):
        return form.iface.dameUsuarios(email)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def startstop(self, oParam, cursor):
        return form.iface.startstop(self, oParam, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def completar_tarea(self, cursor):
        return form.iface.completar_tarea(self, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def incrementar_dia(self, cursor):
        return form.iface.incrementar_dia(self, cursor)

    def bChCursor(fN, cursor):
        return form.iface.bChCursor(fN, cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getTareasUsuario(self, oParam):
        return form.iface.getTareasUsuario(oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def borrar_tarea(self, oParam, cursor):
        return form.iface.borrar_tarea(self, oParam, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def gotoGestionarTiempo(self, cursor):
        return form.iface.gotoGestionarTiempo(self, cursor)

    def commonCalculateField(fN, curP):
        return form.iface.commonCalculateField(fN, curP)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def verTrackingTarea(self, cursor):
        return form.iface.verTrackingTarea(cursor)

    @helpers.decoradores.accion()
    def gototarea(self):
        return form.iface.gotoTarea(self)

    @helpers.decoradores.accion(tipo="O")
    def gotoNewRecordAnotacion(self):
        return form.iface.gotoNewRecordAnotacion()

    def queryGrid_renegociacion(model):
        return form.iface.queryGrid_renegociacion(model)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getParticipantesProyecto(self, oParam):
        return form.iface.getParticipantesProyecto(self, oParam)


# @class_declaration gt_tareas #
class gt_tareas(gesttare_gt_tareas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_tareas_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
