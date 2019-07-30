
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

    def __init__(self, context=None):
        super().__init__(context)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

