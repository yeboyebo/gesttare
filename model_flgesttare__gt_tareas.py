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

    @helpers.decoradores.accion(aqparam=["oParam"])
    def uploadFileTarea(self, oParam):
        return form.iface.uploadFileTarea(self, oParam)

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

    def ren_field_proyecto_espera(self):
        return form.iface.ren_field_proyecto_espera(self)

    def field_completaIcon(self):
        return form.iface.field_completaIcon(self)

    def field_trackingIcon(self):
        return form.iface.field_trackingIcon(self)

    def field_usuario(self):
        return form.iface.field_usuario(self)

    def field_completaTitle(self):
        return form.iface.field_completaTitle(self)

    def color_fecha(self):
        return form.iface.color_fecha(self)

    def color_fechaentrega(self):
        return form.iface.color_fechaentrega(self)

    def ren_color_fecha(self):
        return form.iface.ren_color_fecha(self)

    def ren_color_fechaentrega(self):
        return form.iface.ren_color_fechaentrega(self)

    def ren_color_fecha_espera(self):
        return form.iface.ren_color_fecha_espera(self)

    def ren_color_fechaentrega(self):
        return form.iface.ren_color_fechaentrega_espera(self)

    def color_nombre(self):
        return form.iface.color_nombre(self)

    def color_nombreProyecto(self):
        return form.iface.color_nombreProyecto(self)

    def color_fondo_estado(self):
        return form.iface.color_fondo_estado(self)

    def color_fondo_estado_revision(self):
        return form.iface.color_fondo_estado_revision(self)

    def color_responsable(self):
        return form.iface.color_responsable(self)

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

    def createinbox(oParam):
        return form.iface.createinbox(oParam)

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
    def abrir_tarea(self, cursor):
        return form.iface.abrir_tarea(self, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def incrementar_dia(self, cursor):
        return form.iface.incrementar_dia(self, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def ejecucion_hoy(self, cursor):
        return form.iface.ejecucion_hoy(self, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def un_dia(self, cursor):
        return form.iface.un_dia(self, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def semana_siguiente(self, cursor):
        return form.iface.semana_siguiente(self, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def elegir_fecha(self, cursor):
        return form.iface.elegir_fecha(self, cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def fecha_elegida(self, oParam, cursor):
        return form.iface.fecha_elegida(self, oParam, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def quitar_fecha_modal(self, cursor):
        return form.iface.quitar_fecha_modal(self, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def quitar_fecha_espera(self, cursor):
        return form.iface.quitar_fecha_espera(self, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def quitar_fecha_hacer(self, cursor):
        return form.iface.quitar_fecha_hacer(self, cursor)

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

    @helpers.decoradores.accion(aqparam=["oParam"])
    def gotoReturnActualizacion(self, oParam):
        return form.iface.gotoReturnActualizacion(oParam)

    def revisar_indicadores(self, usuario):
        return form.iface.revisar_indicadores(usuario)

    def revisar_tareas_atrasadas(self, usuario):
        return self.ctx.revisar_tareas_atrasadas(self, usuario)

    # @helpers.decoradores.accion(tipo="O", aqparam=["oParam"])
    @helpers.decoradores.accion(aqparam=["oParam"])
    def gotoNewRecordAnotacion(self, oParam):
        return form.iface.gotoNewRecordAnotacion(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def gotoNewRecordRecordatorioAtrasada(self, oParam):
        return form.iface.gotoNewRecordRecordatorioAtrasada(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def gotoNewRecordRecordatorioBandeja(self, oParam):
        return form.iface.gotoNewRecordRecordatorioBandeja(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def gotoNewRecordRecordatorioEspera(self, oParam):
        return form.iface.gotoNewRecordRecordatorioEspera(oParam)
    
    def queryGrid_renegociacion(model):
        return form.iface.queryGrid_renegociacion(model)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_revisionTareas(model):
        return form.iface.queryGrid_revisionTareas(model)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_revisionTareasTreinta(model):
        return form.iface.queryGrid_revisionTareasTreinta(model)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getParticipantesProyecto(self, oParam):
        return form.iface.getParticipantesProyecto(self, oParam)

    # @helpers.decoradores.accion(tipo="O", aqparam=["oParam"])
    @helpers.decoradores.accion(aqparam=["oParam"])
    def gotonewrecordtarea(self, oParam):
        return form.iface.gotonewrecordtarea(oParam)

    def drawif_completartarea(cursor):
        return form.iface.drawif_completartarea(cursor)

    def drawif_checkAdjuntos(cursor):
        return form.iface.drawif_checkAdjuntos(cursor)

    def drawif_checkActu2(cursor):
        return form.iface.drawif_checkActu2(cursor)

    def drawif_checkNormal(cursor):
        return form.iface.drawif_checkNormal(cursor)

    def drawif_abrirtarea(cursor):
        return form.iface.drawif_abrirtarea(cursor)

    def drawif_iniciartarea(cursor):
        return form.iface.drawif_iniciartarea(cursor)

    def drawif_parartarea(cursor):
        return form.iface.drawif_parartarea(cursor)

    def drawif_trackingplay(cursor):
        return form.iface.drawif_trackingplay(cursor)

    def drawif_trackingpause(cursor):
        return form.iface.drawif_trackingpause(cursor)

    def field_verConvertirTarea(self):
        return form.iface.field_verConvertirTarea(self)

    def field_verConvertirTareaA(self):
        return form.iface.field_verConvertirTareaA(self)

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def verTarea(self, cursor):
        return form.iface.verTarea(self, cursor)

    def field_adjunto(self):
        return form.iface.field_adjunto(self)

    def validateCursor(self):
        return form.iface.validateCursor(self)

    @helpers.decoradores.accion(tipo="O")
    def gotomomentos(self):
        return form.iface.gotomomentos()

    @helpers.decoradores.accion(tipo="O")
    def gotoquimera(self):
        return form.iface.gotoquimera()

    @helpers.decoradores.accion(aqparam=["oParam"])
    def opciones_recordatorio(self, oParam):
        return form.iface.opciones_recordatorio(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def opciones_recordatorio_anotar(self, oParam):
        return form.iface.opciones_recordatorio_anotar(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def opciones_recordatorio_planear(self, oParam):
        return form.iface.opciones_recordatorio_planear(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def opciones_recordatorio_analizar(self, oParam):
        return form.iface.opciones_recordatorio_analizar(oParam)



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
