# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *


class gesttare(interna):

    def gesttare_initValidation(self, name, data=None):
        response = True
        return response

    def gesttare_iniciaValoresLabel(self, model=None, template=None, cursor=None):
        labels = {}
        return labels

    def gesttare_bChLabel(self, fN=None, cursor=None):
        labels = {}
        return labels

    def gesttare_getFilters(self, model, name, template=None):
        filters = []
        return filters

    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        return fields

    def gesttare_getDesc(self):
        desc = "descripcion"
        return desc

    def __init__(self, context=None):
        super(gesttare, self).__init__(context)

    def initValidation(self, name, data=None):
        return self.ctx.gesttare_initValidation(name, data=None)

    def iniciaValoresLabel(self, model=None, template=None, cursor=None):
        return self.ctx.gesttare_iniciaValoresLabel(model, template, cursor)

    def bChLabel(self, fN=None, cursor=None):
        return self.ctx.gesttare_bChLabel(fN, cursor)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()


# @class_declaration head #
class head(gesttare):

    def __init__(self, context=None):
        super(head, self).__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super(ifaceCtx, self).__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
