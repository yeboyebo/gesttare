
# @class_declaration gesttare_gd_documentos #
class gesttare_gd_documentos(interna_gd_documentos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def borrarAdjuntoTarea(self, oParam):
        return form.iface.borrarAdjuntoTarea(self, oParam)

