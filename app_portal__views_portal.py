
# @class_declaration gesttare #
class gesttare(yblogin_sass):

    def gesttare_forbiddenError(self, request):
        return HttpResponseRedirect("/gesttare/gt_tareas/custom/denegado")

    def __init__(self, context=None):
        super().__init__(context)

    def forbiddenError(self, request):
        return self.iface.gesttare_forbiddenError(request)

