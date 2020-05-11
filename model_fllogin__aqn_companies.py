
# @class_declaration gesttare_aqn_companies #
class gesttare_aqn_companies(yblogin_aqn_companies, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_periodicidad(self):
        return form.iface.field_periodicidad(self)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def verPlanes(self, cursor):
        return form.iface.verPlanes(self, cursor)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def mailTo(self, cursor):
        return form.iface.mailTo(self, cursor)

