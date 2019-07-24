# @class_declaration interna_gt_controldiario #
import importlib

from YBUTILS.viewREST import helpers

from models.flgesttare import models as modelos


class interna_gt_controldiario(modelos.mtd_gt_controldiario, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_controldiario #
class gesttare_gt_controldiario(interna_gt_controldiario, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_usuario(self):
        return form.iface.field_usuario(self)

    def drawif_validar(cursor):
        return form.iface.drawif_validar(cursor)

    def drawif_nuevotramo(cursor):
        return form.iface.drawif_nuevotramo(cursor)

    def drawif_horasextra(cursor):
        return form.iface.drawif_horasextra(cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def validar(self, oParam, cursor):
        return form.iface.validar(self, oParam, cursor)

    def bChCursor(fN, cursor):
        return form.iface.bChCursor(fN, cursor)


# @class_declaration gt_controldiario #
class gt_controldiario(gesttare_gt_controldiario, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_controldiario_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
