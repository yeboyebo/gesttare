
# @class_declaration gesttare_aqn_user #
class gesttare_aqn_user(yblogin_aqn_user, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getUsuariosProyecto(self, oParam):
        return form.iface.getUsuariosProyecto(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getParticipantesProyecto(self, oParam):
        return form.iface.getParticipantesProyecto(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getParticProyectosUsu(self, oParam):
        return form.iface.getParticProyectosUsu(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getParticCompaniaUsu(self, oParam):
        return form.iface.getParticCompaniaUsu(oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def desactivar_usuario(self, oParam, cursor):
        return form.iface.desactivar_usuario(self, oParam, cursor)

    def checkCambiaPassword(cursor):
        return form.iface.checkCambiaPassword(cursor)

    def checkDrawUser(cursor):
        return form.iface.checkDrawUser(cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def generaAnalisisGraphic(self, model, template):
        return form.iface.generaAnalisisGraphic(model, template)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getAnalisisGraphic(self, oParam):
        print("???????????????")
        return form.iface.getAnalisisGraphic(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_pruebagrafico(model, filters):
        return form.iface.queryGrid_pruebagrafico(model, filters)

