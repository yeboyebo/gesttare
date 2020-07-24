# @class_declaration interna_gt_comentarios #
from YBUTILS.viewREST import helpers
from models.flgesttare import models as modelos
import importlib


class interna_gt_comentarios(modelos.mtd_gt_comentarios, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gesttare_gt_comentarios #
class gesttare_gt_comentarios(interna_gt_comentarios, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_adjunto(self):
        return form.iface.field_adjunto(self)

    def field_nombreUsuario(self):
        return form.iface.field_nombreUsuario(self)

    def field_observaIcon(self):
        return form.iface.field_observaIcon(self)

    def field_observaTitle(self):
        return form.iface.field_observaTitle(self)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def comentario_publico(self, oParam, cursor):
        return form.iface.comentario_publico(self, oParam, cursor)


# @class_declaration gt_comentarios #
class gt_comentarios(gesttare_gt_comentarios, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flgesttare.gt_comentarios_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
