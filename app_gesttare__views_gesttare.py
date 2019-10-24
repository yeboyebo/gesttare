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
        idcompany = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(username))
        tengomodulo = qsatype.FLUtil.quickSqlSelect("aqn_modulescompanies", "id", "idcompany = '{}'".format(idcompany))

        if not tareaactiva:
            if not tengomodulo:
                return {}
            return {
                    "appConfiguration": [{
                        "key": "controlhorario",
                        "text": "Control horario",
                        "href": "/gesttare/gt_controlhorario/custom/control_horario"
                    }]
                }

        nombre_proyecto = "// Proyecto: "
        nombre_tarea = qsatype.FLUtil.quickSqlSelect("gt_tareas", "nombre", "idtarea = {}".format(tareaactiva))
        nombre_proyecto += qsatype.FLUtil.quickSqlSelect("gt_proyectos p INNER JOIN gt_tareas ta ON p.codproyecto = ta.codproyecto", "p.nombre", "ta.idtarea = {}".format(tareaactiva))

        appinfo = {
            "data": [{
                "pk": tareaactiva,
                "idtarea": tareaactiva,
                "nombreactiva": nombre_tarea,
                "nombreproyecto": nombre_proyecto
            }],
            "layout": {
                "tareaActiva": {
                    "componente": "YBTable",
                    "paginacion": False,
                    "type": "json",
                    "hideheader": True,
                    "border": False,
                    "style": {
                        "fontWeight": "bold"
                    },
                    "prefix": "appinfo",
                    "columns": [
                        {
                            "tipo": "act",
                            "key": "startstop",
                            "label": "Timetracking",
                            "success": [{"slot": "refrescar"}]
                        },
                        {"tipo": "field", "key": "nombreactiva", "label": "Tarea activa"},
                        {"tipo": "field", "key": "nombreproyecto", "label": "Tarea activa"}
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


        if tengomodulo:
            appinfo["appConfiguration"] =  [{
                    "key": "controlhorario",
                    "text": "Control horario",
                    "href": "/gesttare/gt_controlhorario/custom/control_horario"
                }]

        return appinfo

    def gesttare_get_app_drawIf(self, drawIf, pk):
        return {"YBNavBarActions": {"pauseControlHorario": "drawIfPauseControl", "startControlHorario": "drawIfstartControl"}}

    def gesttare_drawIfPauseControl(self, cursor):
        usuario = qsatype.FLUtil.nameUser() 
        tramoactivo = qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idusuario = {} AND horafin IS NULL".format(usuario))
        idcompany = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(usuario))
        tengomodulo = qsatype.FLUtil.quickSqlSelect("aqn_modulescompanies", "id", "idcompany = '{}'".format(idcompany))
        if not tengomodulo:
            return "hidden"
        if not tramoactivo:
            return "hidden"
        return True

    def gesttare_drawIfstartControl(self, cursor):
        usuario = qsatype.FLUtil.nameUser() 
        idcompany = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(usuario))
        tengomodulo = qsatype.FLUtil.quickSqlSelect("aqn_modulescompanies", "id", "idcompany = '{}'".format(idcompany))
        if not tengomodulo:
            return "hidden"
        if qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idusuario = {} AND horafin IS NULL".format(usuario)):
            return "hidden"
        return True

    def __init__(self, context=None):
        super().__init__(context)

    def get_app_info(self, model, data):
        return self.ctx.gesttare_get_app_info(model, data)

    def get_app_drawIf(self, drawIf, pk):
        return self.ctx.gesttare_get_app_drawIf(drawIf, pk)

    def drawIfPauseControl(self, cursor):
        return self.ctx.gesttare_drawIfPauseControl(cursor)

    def drawIfstartControl(self, cursor):
        return self.ctx.gesttare_drawIfstartControl(cursor)


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
