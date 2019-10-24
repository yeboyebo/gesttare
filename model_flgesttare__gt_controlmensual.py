# @class_declaration interna_gt_controlmensual #
import importlib

from YBUTILS.viewREST import helpers

from models.flgesttare import models as modelos


class interna_gt_controlmensual(modelos.mtd_gt_controlmensual, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_controlmensual #
class gesttare_gt_controlmensual(interna_gt_controlmensual, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_usuario(self):
        return form.iface.field_usuario(self)

    def color_usuario(self):
        return form.iface.color_usuario(self)

    def field_mesanyo(self):
        return form.iface.field_mesanyo(self)

    def field_razonsocial(self):
        return form.iface.field_razonsocial(self)

    def field_cif(self):
        return form.iface.field_cif(self)

    def field_ccc(self):
        return form.iface.field_ccc(self)

    def field_nombreap(self):
        return form.iface.field_nombreap(self)

    def field_nif(self):
        return form.iface.field_nif(self)

    def field_naf(self):
        return form.iface.field_naf(self)

    def drawif_validar_user(cursor):
        return form.iface.drawif_validar_user(cursor)

    def drawif_validar_admin(cursor):
        return form.iface.drawif_validar_admin(cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def validar_user(self, oParam, cursor):
        return form.iface.validar_user(self, oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def validar_admin(self, oParam, cursor):
        return form.iface.validar_admin(self, oParam, cursor)

    def drawif_desbloquear_user(cursor):
        return form.iface.drawif_desbloquear_user(cursor)

    def drawif_desbloquear_admin(cursor):
        return form.iface.drawif_desbloquear_admin(cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def desbloquear_user(self, cursor):
        return form.iface.desbloquear_user(self, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def desbloquear_admin(self, cursor):
        return form.iface.desbloquear_admin(self, cursor)


# @class_declaration gt_controlmensual #
class gt_controlmensual(gesttare_gt_controlmensual, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_controlmensual_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
