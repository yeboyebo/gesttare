# @class_declaration interna_gt_controlhorario #
import importlib

from YBUTILS.viewREST import helpers

from models.flgesttare import models as modelos


class interna_gt_controlhorario(modelos.mtd_gt_controlhorario, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_controlhorario #
class gesttare_gt_controlhorario(interna_gt_controlhorario, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_control_diario(model, filters):
        return form.iface.queryGrid_control_diario(model, filters)

    @helpers.decoradores.accion(aqparam=[])
    def start(self):
        return form.iface.start(self)

    @helpers.decoradores.accion(aqparam=[])
    def pause(self):
        return form.iface.pause(self)

    def drawif_controldiario(cursor):
        return form.iface.drawif_controldiario(cursor)

    def drawif_controlmensual(cursor):
        return form.iface.drawif_controlmensual(cursor)

    def drawif_botondiario(cursor):
        return form.iface.drawif_botondiario(cursor)

    def drawif_botonmensual(cursor):
        return form.iface.drawif_botonmensual(cursor)

    def drawif_horaeditable(cursor):
        return form.iface.drawif_horaeditable(cursor)

    def drawif_idusuariofilter(cursor):
        return form.iface.drawif_idusuariofilter(cursor)

    @helpers.decoradores.accion(aqparam=[])
    def set_estado_diario(self):
        return form.iface.set_estado("diario")

    @helpers.decoradores.accion(aqparam=[])
    def set_estado_mensual(self):
        return form.iface.set_estado("mensual")


# @class_declaration gt_controlhorario #
class gt_controlhorario(gesttare_gt_controlhorario, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_controlhorario_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
