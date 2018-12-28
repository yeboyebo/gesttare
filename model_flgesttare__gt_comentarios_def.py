# @class_declaration interna #
from YBLEGACY import qsatype
from YBUTILS import gesDoc


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *


class gesttare(interna):

    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        fields = [{'verbose_name': 'adjunto', 'func': 'field_adjunto'}]
        return fields

    def gesttare_getDesc(self):
        return None

    def gesttare_field_adjunto(self, model):
        nombre = None
        file = gesDoc.getFiles("gt_comentarios", model.pk)
        if file:
            return file["nombre"]
        return nombre

    def __init__(self, context=None):
        super().__init__(context)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def field_adjunto(self, model):
        return self.ctx.gesttare_field_adjunto(model)


# @class_declaration head #
class head(gesttare):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
