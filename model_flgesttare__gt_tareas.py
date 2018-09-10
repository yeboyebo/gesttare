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

    @helpers.decoradores.accion(aqparam=["oParam"])
    def actNuevoComentario(self, oParam):
        return form.iface.actNuevoComentario(self, oParam)

    def queryGrid_calendarioTareas(model):
        return form.iface.queryGrid_calendarioTareas(model)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getListaTarea(self, oParam):
        return form.iface.getListaTarea(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def uploadFile(self, oParam):
        return True
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


# @class_declaration gt_tareas #
class gt_tareas(gesttare_gt_tareas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


definitions = importlib.import_module("models.flgesttare.gt_tareas_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
