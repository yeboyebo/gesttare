# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *


class gesttare(interna):

    def gesttare_getDesc(self):
        return None

    def gesttare_getForeignFields(self, model, template=None):
        fields = [
            {'verbose_name': 'usuario', 'func': 'field_usuario'}
        ]

        return fields

    def gesttare_field_usuario(self, model):
        nombre_usuario = ""

        try:
            if not model.idusuario:
                return nombre_usuario
            nombre_usuario = model.idusuario.usuario
        except Exception:
            pass

        return nombre_usuario

    def gesttare_check_permissions(self, model, prefix, pk, template, acl, accion):
        if template == "formRecord":
            my_name = qsatype.FLUtil.nameUser()
            if my_name == "admin":
                return True

            reg_name = qsatype.FLUtil.sqlSelect("gt_controldiario", "idusuario", "idc_diario = {}".format(pk))
            if my_name == str(reg_name):
                return True

            im_superuser = qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(my_name))
            if not im_superuser:
                return False

            my_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(my_name))
            reg_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(reg_name))
            if my_company == reg_company:
                return True

            return False

        return True

    def gesttare_getFilters(self, model, name, template=None):
        filters = []

        if name == "regusuario":
            user_name = qsatype.FLUtil.nameUser()
            filters = [{"criterio": "idusuario__exact", "valor": user_name, "tipo": "q"}]

            if not qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(user_name)):
                return filters

            usuarios = []
            user_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(user_name))

            q = qsatype.FLSqlQuery()
            q.setSelect("idusuario")
            q.setFrom("aqn_user")
            q.setWhere("idcompany = {}".format(user_company))

            if not q.exec_():
                return False

            while q.next():
                usuarios.append(q.value(0))

            filters.append({"criterio": "idusuario__in", "valor": usuarios, "tipo": "q"})

        return filters

    def gesttare_drawif_validar(self, cursor):
        if cursor.valueBuffer("validado"):
            return "disabled"

        if qsatype.FLUtil.nameUser() != str(cursor.valueBuffer("idusuario")):
            return "disabled"

        # if not cursor.valueBuffer("horasextra"):
        #     return "disabled"

        if qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idc_diario = {} AND horafin IS NULL".format(cursor.valueBuffer("idc_diario"))):
            return "disabled"

    def gesttare_drawif_nuevotramo(self, cursor):
        if cursor.valueBuffer("validado"):
            return "hidden"

        if qsatype.FLUtil.nameUser() != str(cursor.valueBuffer("idusuario")):
            return "hidden"

    def gesttare_drawif_horasextra(self, cursor):
        if cursor.valueBuffer("validado"):
            return "disabled"

        if qsatype.FLUtil.nameUser() != str(cursor.valueBuffer("idusuario")):
            return "disabled"

    def gesttare_validar(self, model, cursor):
        if cursor.valueBuffer("validado"):
            return True

        cursor.setValueBuffer("validado", True)
        if not cursor.commitBuffer():
            return False

        return True

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def field_usuario(self, model):
        return self.ctx.gesttare_field_usuario(model)

    def check_permissions(self, model, prefix, pk, template, acl, accion=None):
        return self.ctx.gesttare_check_permissions(model, prefix, pk, template, acl, accion)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def drawif_validar(self, cursor):
        return self.ctx.gesttare_drawif_validar(cursor)

    def drawif_nuevotramo(self, cursor):
        return self.ctx.gesttare_drawif_nuevotramo(cursor)

    def drawif_horasextra(self, cursor):
        return self.ctx.gesttare_drawif_horasextra(cursor)

    def validar(self, model, cursor):
        return self.ctx.gesttare_validar(model, cursor)


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
