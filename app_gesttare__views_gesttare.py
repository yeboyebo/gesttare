# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
class gesttare(interna):

    def gesttare_get_app_info(self, model, data):
        username = qsatype.FLUtil.nameUser()
        tareaactiva = qsatype.FLUtil.quickSqlSelect("aqn_user", "idtareaactiva", "idusuario = '{}'".format(username))

        if not tareaactiva:
            return None

        nombre_tarea = qsatype.FLUtil.quickSqlSelect("gt_tareas", "nombre", "idtarea = {}".format(tareaactiva))

        return {
            "data": [{
                "pk": tareaactiva,
                "idtarea": tareaactiva,
                "nombreactiva": nombre_tarea
            }],
            "layout": {
                "tareaActiva": {
                    "componente": "YBTable",
                    "paginacion": False,
                    "type": "json",
                    "hideheader": True,
                    "border": False,
                    "prefix": "appinfo",
                    "columns": [
                        {
                            "tipo": "act",
                            "key": "startstop",
                            "label": "Timetracking",
                            "success": [{"slot": "refrescar"}]
                        },
                        {"tipo": "field", "key": "nombreactiva", "label": "Tarea activa"}
                    ]
                }
            },
            "acciones": {
                "startstop": {
                    "action": "legacy",
                    "prefix": "gt_tareas",
                    "serverAction": "startstop",
                    "icon": "alarm"
                }
            }
        }

    def __init__(self, context=None):
        super().__init__(context)

    def get_app_info(self, model, data):
        return self.ctx.gesttare_get_app_info(model, data)


# @class_declaration head #
class head(gesttare):

    def __init__(self, context=None):
        super().__init__(context)

    def uploadFile(self, request):
        print("__________________")
        print(request.FILES)
        return {"obj": True}

# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
