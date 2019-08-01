# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *


class gesttare(interna):

    def gesttare_getForeignFields(self, model, template=None):
        fields = [{'verbose_name': 'nombre', 'func': 'field_nombre'}]
        return fields

    def gesttare_getDesc(self):
        return "nombre"

    def gesttare_get_model_info(self, model, data, pag, where_filter):
        participantes = "Participantes: "
        participantes = ""
        for part in data:
            user = qsatype.FLUtil.sqlSelect(u"aqn_user", u"usuario", ustr(u"idusuario = '", part["idusuario"], "'"))
            participantes = participantes + user + ", "
        participantes = participantes[:len(participantes) - 2]
        return {"participantesGrid": participantes}

    def gesttare_field_nombre(self, model):
        nombre = ""
        try:
            nombre = model.idusuario.usuario
        except Exception as e:
            print(e)
        return nombre

    def __init__(self, context=None):
        super().__init__(context)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def get_model_info(self, model, data, pag, where_filter):
        return self.ctx.gesttare_get_model_info(model, data, pag, where_filter)

    def field_nombre(self, model):
        return self.ctx.gesttare_field_nombre(model)


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
