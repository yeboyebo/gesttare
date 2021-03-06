
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
    def getUsuTutelados(self, oParam):
        return form.iface.getUsuTutelados(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getParticCompaniaUsu(self, oParam):
        return form.iface.getParticCompaniaUsu(oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def activar(self, oParam, cursor):
        return form.iface.activar(self, oParam, cursor)

    def checkCambiaPassword(cursor):
        return form.iface.checkCambiaPassword(cursor)

    def checkDrawUser(cursor):
        return form.iface.checkDrawUser(cursor)

    def checkResponsableDraw(cursor):
        return form.iface.checkResponsableDraw(cursor)

    def field_nombre(self):
        return form.iface.field_nombre(self)

    def field_nombreform(self):
        return form.iface.field_nombreform(self)

    def color_usuario(self):
        return form.iface.color_usuario(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def generaAnalisisGraphic(self, model, template):
        return form.iface.generaAnalisisGraphic(model, template)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getAnalisisGraphic(self, oParam):
        return form.iface.getAnalisisGraphic(oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_tareasMasTiempo(model, filters):
        return form.iface.queryGrid_tareasMasTiempo(model, filters)

    def drawif_idusuariofilter(cursor):
        return form.iface.drawif_idusuariofilter(cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def dameEmailCreaAnotacion(self, oParam, cursor):
        return form.iface.dameEmailCreaAnotacion(oParam, cursor)

    def field_completaTitle(self):
        return form.iface.field_completaTitle(self)

    def field_completaIcon(self):
        return form.iface.field_completaIcon(self)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def activar_nomenclatura(self, cursor):
        return form.iface.activar_nomenclatura(cursor)

