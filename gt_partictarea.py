# @class_declaration interna_gt_partictarea #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_partictarea(modelos.mtd_gt_partictarea, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_partictarea #
class gesttare_gt_partictarea(interna_gt_partictarea, helpers.MixinConAcciones):
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


# @class_declaration gt_partictarea #
class gt_partictarea(gesttare_gt_partictarea, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


definitions = importlib.import_module("models.flgesttare.gt_partictarea_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
