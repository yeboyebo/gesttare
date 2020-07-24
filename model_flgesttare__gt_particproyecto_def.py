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
        fields = [{'verbose_name': 'nombre', 'func': 'field_nombre'}, {'verbose_name': 'Color_nombre_participante', 'func': 'color_nombre_participante'}]
        return fields

    def gesttare_getDesc(self):
        return None

    def gesttare_get_model_info(self, model, data, pag, where_filter):
        participantes = "Participantes: "
        participantes = ""
        for part in data:
            user = qsatype.FLUtil.sqlSelect("aqn_user", "usuario", "idusuario = '{}'".format(part["idusuario"]))
            if user:
                participantes = participantes + user + ", "
        participantes = participantes[:len(participantes) - 2]
        return {"participantesGrid": participantes}

    def gesttare_field_nombre(self, model):
        usuario = ""
        try:
            usuario = model.idusuario.usuario
        except Exception:
            pass
        return usuario

    def gesttare_color_nombre_participante(self, model):
        username = model.idusuario.idusuario
        id_company = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(username))

        tipo_participante = qsatype.FLUtil.quickSqlSelect("gt_particproyecto", "tipo", "idusuario = '{}' AND idproyecto = {}".format(username, str(model.idproyecto.idproyecto)))
        if tipo_participante == "observador":
            return "OBSER "
        if model.idproyecto.idcompany.idcompany != id_company:
            return "COL "
        else:
            return "INTERNO_EMPRESA "

        return ""

    def gesttare_borrarPartic(self, oParam, cursor):
        idproyecto = cursor.valueBuffer("idproyecto")
        usuario = qsatype.FLUtil.nameUser()
        responsable = qsatype.FLUtil.sqlSelect("gt_proyectos", "idresponsable", "idproyecto = '{}'".format(idproyecto))
        resul = {}
        if int(usuario) == responsable:
            cursor.setModeAccess(cursor.Del)
            cursor.refreshBuffer()
            if not cursor.commitBuffer():
                return False
            resul["return_data"] = False
            resul["msg"] = "Participante eliminado correctamente"
        else:
            resul["return_data"] = False
            resul["msg"] = "Solo puede eliminar participantes el responsable de proyecto"
        return resul

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

    def borrarPartic(self, oParam, cursor):
        return self.ctx.gesttare_borrarPartic(oParam, cursor)

    def color_nombre_participante(self, model):
        return self.ctx.gesttare_color_nombre_participante(model)


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
