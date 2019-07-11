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
            {'verbose_name': 'mesanyo', 'func': 'field_mesanyo'},
            {'verbose_name': 'usuario', 'func': 'field_usuario'}
        ]

        if template == "formRecord":
            fields.append({'verbose_name': 'Razón social', 'func': 'field_razonsocial'})
            fields.append({'verbose_name': 'CIF', 'func': 'field_cif'})
            fields.append({'verbose_name': 'CCC', 'func': 'field_ccc'})
            fields.append({'verbose_name': 'NombreAP', 'func': 'field_nombreap'})
            fields.append({'verbose_name': 'NIF', 'func': 'field_nif'})
            fields.append({'verbose_name': 'NAF', 'func': 'field_naf'})

        return fields

    def gesttare_field_mesanyo(self, model):
        if not model.mes:
            return ""
        if not model.anyo:
            return ""
        return "{} {}".format(self.iface.get_mes(model.mes), model.anyo)

    def gesttare_field_nombreap(self, model):
        try:
            if not model.idusuario:
                return ""
            if not model.idusuario.nombre and not model.idusuario.apellidos:
                return model.idusuario.usuario
            return "{} {}".format(model.idusuario.nombre, model.idusuario.apellidos)
        except Exception:
            return ""

    def gesttare_field_usuario(self, model):
        try:
            if not model.idusuario:
                return ""
            return model.idusuario.usuario
        except Exception:
            return ""

    def gesttare_field_razonsocial(self, model):
        try:
            if not model.idusuario:
                return ""
            if not model.idusuario.idcompany:
                return ""

            return model.idusuario.idcompany.descripcion
        except Exception:
            return ""

    def gesttare_field_cif(self, model):
        try:
            if not model.idusuario:
                return ""
            if not model.idusuario.idcompany:
                return ""

            return model.idusuario.idcompany.cif
        except Exception:
            return ""

    def gesttare_field_ccc(self, model):
        try:
            if not model.idusuario:
                return ""
            if not model.idusuario.idcompany:
                return ""

            return model.idusuario.idcompany.ccc
        except Exception:
            return ""

    def gesttare_field_nif(self, model):
        try:
            if not model.idusuario:
                return ""
            return model.idusuario.nif
        except Exception:
            return ""

    def gesttare_field_naf(self, model):
        try:
            if not model.idusuario:
                return ""
            return model.idusuario.naf
        except Exception:
            return ""

    def gesttare_check_permissions(self, model, prefix, pk, template, acl, accion):
        if template == "formRecord":
            my_name = qsatype.FLUtil.nameUser()
            if my_name == "admin":
                return True

            reg_name = qsatype.FLUtil.sqlSelect("gt_controlmensual", "idusuario", "idc_mensual = {}".format(pk))
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

    def gesttare_get_mes(self, mes):
        if len(mes) < 2 or isNaN(int(mes)):
            return mes

        array_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        return array_meses[int(mes) - 1]

    def gesttare_drawif_validar_user(self, cursor):
        if cursor.valueBuffer("validado_user"):
            return "disabled"

        if qsatype.FLUtil.nameUser() != str(cursor.valueBuffer("idusuario")):
            return "disabled"

        if qsatype.FLUtil().quickSqlSelect("gt_controldiario", "idc_diario", "idc_mensual = {} AND NOT validado".format(cursor.valueBuffer("idc_mensual"))):
            return "disabled"

    def gesttare_drawif_validar_admin(self, cursor):
        if not cursor.valueBuffer("validado_user"):
            return "disabled"

        if cursor.valueBuffer("validado_admin"):
            return "disabled"

        my_name = qsatype.FLUtil.nameUser()
        if my_name == "admin":
            return ""

        im_superuser = qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(my_name))
        if not im_superuser:
            return "disabled"

        reg_name = qsatype.FLUtil.sqlSelect("gt_controlmensual", "idusuario", "idc_mensual = {}".format(cursor.valueBuffer("idusuario")))
        my_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(my_name))
        reg_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(reg_name))
        if my_company != reg_company:
            return "disabled"

    def gesttare_validar_user(self, model, cursor):
        if cursor.valueBuffer("validado_user"):
            return True

        cursor.setValueBuffer("validado_user", True)
        if not cursor.commitBuffer():
            return False

        return True

    def gesttare_validar_admin(self, model, cursor):
        if cursor.valueBuffer("validado_admin"):
            return True

        idadmin = qsatype.FLUtil.nameUser()

        cursor.setValueBuffer("idadmin", idadmin)
        cursor.setValueBuffer("validado_admin", True)
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

    def field_mesanyo(self, model):
        return self.ctx.gesttare_field_mesanyo(model)

    def field_razonsocial(self, model):
        return self.ctx.gesttare_field_razonsocial(model)

    def field_cif(self, model):
        return self.ctx.gesttare_field_cif(model)

    def field_ccc(self, model):
        return self.ctx.gesttare_field_ccc(model)

    def field_nombreap(self, model):
        return self.ctx.gesttare_field_nombreap(model)

    def field_nif(self, model):
        return self.ctx.gesttare_field_nif(model)

    def field_naf(self, model):
        return self.ctx.gesttare_field_naf(model)

    def check_permissions(self, model, prefix, pk, template, acl, accion=None):
        return self.ctx.gesttare_check_permissions(model, prefix, pk, template, acl, accion)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def get_mes(self, mes):
        return self.ctx.gesttare_get_mes(mes)

    def drawif_validar_user(self, cursor):
        return self.ctx.gesttare_drawif_validar_user(cursor)

    def drawif_validar_admin(self, cursor):
        return self.ctx.gesttare_drawif_validar_admin(cursor)

    def validar_user(self, model, cursor):
        return self.ctx.gesttare_validar_user(model, cursor)

    def validar_admin(self, model, cursor):
        return self.ctx.gesttare_validar_admin(model, cursor)


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
