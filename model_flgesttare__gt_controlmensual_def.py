# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
from models.flgesttare import flgesttare_def


class gesttare(interna):

    def gesttare_getDesc(self):
        return None

    def gesttare_getForeignFields(self, model, template=None):
        fields = [
            {'verbose_name': 'mesanyo', 'func': 'field_mesanyo'},
            {'verbose_name': 'usuario', 'func': 'field_usuario'},
            {'verbose_name': 'Color usuario', 'func': 'color_usuario'}

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
        usuario = "@" 
        try:
            if not model.idusuario:
                return ""
            usuario += model.idusuario.usuario
            return usuario
        except Exception:
            return ""

    def gesttare_field_razonsocial(self, model):
        try:
            if not model.idusuario:
                return ""
            if not model.idusuario.idcompany:
                return ""
            descripcion = qsatype.FLUtil.sqlSelect("aqn_companies", "descripcion", "idcompany = {}".format(model.idusuario.idcompany))    
            # return model.idusuario.idcompany.descripcion
            return descripcion
        except Exception:
            return ""

    def gesttare_field_cif(self, model):
        try:
            if not model.idusuario:
                return ""
            if not model.idusuario.idcompany:
                return ""
            cif = qsatype.FLUtil.sqlSelect("aqn_companies", "cif", "idcompany = {}".format(model.idusuario.idcompany))
            # return model.idusuario.idcompany.cif
            return cif
        except Exception:
            return ""

    def gesttare_field_ccc(self, model):
        try:
            if not model.idusuario:
                return ""
            if not model.idusuario.idcompany:
                return ""
            ccc = qsatype.FLUtil.sqlSelect("aqn_companies", "ccc", "idcompany = {}".format(model.idusuario.idcompany))
            # return model.idusuario.idcompany.ccc
            return ccc
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
            if im_superuser:
                return True

            responsable = qsatype.FLUtil.sqlSelect("aqn_user", "idresponsable", "idusuario = '{}'".format(reg_name))
            if str(responsable) == str(my_name):
                return True

            # my_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(my_name))
            # reg_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(reg_name))
            # if my_company == reg_company:
            #     return True

            return False

        return True

    def gesttare_getFilters(self, model, name, template=None):
        filters = []

        if name == "regusuario":
            user_name = qsatype.FLUtil.nameUser()
            filters = [{"criterio": "idusuario__exact", "valor": user_name, "tipo": "q"}]

            usuarios = []
            user_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(user_name))
            where = "idcompany = {}".format(user_company)
           
            if not qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(user_name)):
                where += " AND idresponsable = '" + user_name + "'"

            q = qsatype.FLSqlQuery()
            q.setSelect("idusuario")
            q.setFrom("aqn_user")
            q.setWhere(where)

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
            return "hidden"

        if qsatype.FLUtil.nameUser() != str(cursor.valueBuffer("idusuario")):
            return "hidden"

        if qsatype.FLUtil().quickSqlSelect("gt_controldiario", "idc_diario", "idc_mensual = {} AND NOT validado".format(cursor.valueBuffer("idc_mensual"))):
            return "disabled"

    def gesttare_drawif_validar_admin(self, cursor):
        my_name = qsatype.FLUtil.nameUser()
        im_superuser = qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(my_name))
        has_responsable = qsatype.FLUtil.sqlSelect("aqn_user", "idresponsable", "idusuario = '{}'".format(cursor.valueBuffer("idusuario")))
        permiso = False
        if has_responsable:
            print(1)
            if str(has_responsable) == str(my_name):
                permiso = True
        elif im_superuser:
            permiso = True

        if not permiso:
            return "hidden"

        if not cursor.valueBuffer("validado_user"):
            return "disabled"

        if cursor.valueBuffer("validado_admin"):
            return "hidden"

        # return "hidden"
        # reg_name = qsatype.FLUtil.sqlSelect("gt_controlmensual", "idusuario", "idc_mensual = {}".format(cursor.valueBuffer("idusuario")))
        # my_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(my_name))
        # reg_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(reg_name))
        # if my_company != reg_company:
        #     return "hidden"

    def gesttare_validar_user(self, model, oParam, cursor):
        if cursor.valueBuffer("validado_user"):
            return True

        if "confirmacion" not in oParam:
            resul = {}
            if cursor.valueBuffer("horasordinarias") < flgesttare_def.iface.time_to_seconds(cursor.valueBuffer("horasextra")):
                resul["status"] = 1
                resul["msg"] = "Las horas extraordinarias no pueden superar el total de tiempo"
                return resul
            resul['status'] = 2
            resul['confirm'] = "Vas a validar el mes con los siguientes datos: " + str(cursor.valueBuffer("horasordinariasstring")) + " como tiempo de trabajo ordinario, y " + str(cursor.valueBuffer("horasextra")) + " como tiempo de trabajo extraordinario. ¿Son correctos los datos?"
            resul["msg"] = "Validado como trabajador"
            return resul
        else:
            now = str(qsatype.Date())
            fecha = now[:10]
            cursor.setValueBuffer("validado_user", True)
            cursor.setValueBuffer("fechavalidadouser", fecha)
            if not cursor.commitBuffer():
                return False

        return True

    def gesttare_validar_admin(self, model, oParam, cursor):
        if cursor.valueBuffer("validado_admin"):
            return True

        if "confirmacion" not in oParam:
            resul = {}
            if cursor.valueBuffer("horasordinarias") < flgesttare_def.iface.time_to_seconds(cursor.valueBuffer("horasextra")):
                resul["status"] = 1
                resul["msg"] = "Las horas extraordinarias no pueden superar el total de tiempo"
                return resul
            nombre = qsatype.FLUtil().quickSqlSelect("aqn_user", "concat(nombre, ' ', apellidos)", "idusuario = {}".format(cursor.valueBuffer("idusuario")))
            resul['status'] = 2
            resul['confirm'] = "Vas a validar el mes de " + nombre + " con los siguientes datos: " + str(cursor.valueBuffer("horasordinariasstring")) + " como tiempo de trabajo ordinario, y " + str(cursor.valueBuffer("horasextra")) + " como tiempo de trabajo extraordinario. ¿Son correctos los datos?"
            resul["msg"] = "Validado como responsable"
            return resul
        else:
            usuario = qsatype.FLUtil.nameUser()
            now = str(qsatype.Date())
            fecha = now[:10]
            cursor.setValueBuffer("idadmin", usuario)
            cursor.setValueBuffer("validado_admin", True)
            cursor.setValueBuffer("idvalidador", usuario)
            cursor.setValueBuffer("fechavalidadoadmin", fecha)
            if not cursor.commitBuffer():
                return False

        return True

    def gesttare_drawif_desbloquear_user(self, cursor):
        if cursor.valueBuffer("validado_admin"):
            return "disabled"

        if not cursor.valueBuffer("validado_user"):
            return "hidden"

        if qsatype.FLUtil.nameUser() != str(cursor.valueBuffer("idusuario")):
            return "hidden"

        if qsatype.FLUtil().quickSqlSelect("gt_controldiario", "idc_diario", "idc_mensual = {} AND NOT validado".format(cursor.valueBuffer("idc_mensual"))):
            return "hidden"

    def gesttare_drawif_desbloquear_admin(self, cursor):
        my_name = qsatype.FLUtil.nameUser()
        im_superuser = qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(my_name))
        has_responsable = qsatype.FLUtil.sqlSelect("aqn_user", "idresponsable", "idusuario = '{}'".format(cursor.valueBuffer("idusuario")))
        permiso = False

        if has_responsable:
            if str(has_responsable) == str(my_name):
                permiso = True
        elif im_superuser:
            permiso = True
 
        if not permiso:
            return "hidden"

        if not cursor.valueBuffer("validado_admin"):
            return "hidden"

        if not cursor.valueBuffer("validado_user"):
            return "disabled"

        if cursor.valueBuffer("validado_admin"):
            return ""

        # reg_name = qsatype.FLUtil.sqlSelect("gt_controlmensual", "idusuario", "idc_mensual = {}".format(cursor.valueBuffer("idusuario")))
        # my_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(my_name))
        # reg_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(reg_name))
        # if my_company != reg_company:
        #     return "hidden"

    def gesttare_desbloquear_user(self, model, cursor):
        if not cursor.valueBuffer("validado_user"):
            return True
        now = str(qsatype.Date())
        fecha = now[:10]
        cursor.setValueBuffer("validado_user", False)
        cursor.setValueBuffer("fechavalidadouser", fecha)
        if not cursor.commitBuffer():
            return False

        return True

    def gesttare_desbloquear_admin(self, model, cursor):
        if not cursor.valueBuffer("validado_admin"):
            return True

        usuario = qsatype.FLUtil.nameUser()
        now = str(qsatype.Date())
        fecha = now[:10]
        cursor.setValueBuffer("idadmin", usuario)
        cursor.setValueBuffer("idvalidador", usuario)
        cursor.setValueBuffer("validado_admin", False)
        cursor.setValueBuffer("fechavalidadoadmin", fecha)
        if not cursor.commitBuffer():
            return False

        return True

    def gesttare_color_usuario(self, model):
        # print(model['aqn_user.usuario'])
        # if (model['aqn_user.usuario']):
        #     return "usuario"

        return "usuario"

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

    def validar_user(self, model, oParam, cursor):
        return self.ctx.gesttare_validar_user(model, oParam, cursor)

    def validar_admin(self, model, oParam, cursor):
        return self.ctx.gesttare_validar_admin(model, oParam, cursor)

    def drawif_desbloquear_user(self, cursor):
        return self.ctx.gesttare_drawif_desbloquear_user(cursor)

    def drawif_desbloquear_admin(self, cursor):
        return self.ctx.gesttare_drawif_desbloquear_admin(cursor)

    def desbloquear_user(self, model, cursor):
        return self.ctx.gesttare_desbloquear_user(model, cursor)

    def desbloquear_admin(self, model, cursor):
        return self.ctx.gesttare_desbloquear_admin(model, cursor)

    def color_usuario(self, model):
        return self.ctx.gesttare_color_usuario(model)

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
