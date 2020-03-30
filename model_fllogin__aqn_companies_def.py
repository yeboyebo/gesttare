
# @class_declaration gesttare #
class gesttare(yblogin):


    def gesttare_getFilters(self, model, name, template=None):
        filters = []
        usuario = qsatype.FLUtil.nameUser()
        if name == 'micompania':
            if usuario == 'master':
                return []
            idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
            return [{'criterio': 'idcompany__exact', 'valor': idcompany}]

        return filters


    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        if template == "formRecord":
            return [{'verbose_name': 'Modalidad de pago', 'func': 'field_periodicidad'}]

        return fields

    def gesttare_field_periodicidad(self, model):
        usuario = qsatype.FLUtil.nameUser()
        id_compania = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(usuario))
        id_plan = qsatype.FLUtil.quickSqlSelect("aqn_companies", "idplan", "idcompany = '{}'".format(id_compania)) or None
        if id_plan and id_plan != 1:
            periodicidad = qsatype.FLUtil.quickSqlSelect("aqn_planes", "modalidad", "idplan = '{}'".format(id_plan)) or None
            return periodicidad
        elif id_plan == 1:
            return "Gratuita"

        return ""

    def gesttare_verPlanes(self, model, cursor):
        url = "/planes/" + str(cursor.valueBuffer("idplan"))
        return url

    def __init__(self, context=None):
        super().__init__(context)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def field_periodicidad(self, model):
        return self.ctx.gesttare_field_periodicidad(model)

    def verPlanes(self, model, cursor):
        return self.ctx.gesttare_verPlanes(model, cursor)

