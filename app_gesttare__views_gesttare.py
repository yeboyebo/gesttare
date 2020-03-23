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
            # if not tengomodulo:
            #     return {}
            # return {
            #         "appConfiguration": [{
            #             "key": "controlhorario",
            #             "text": "Control horario",
            #             "href": "/gesttare/gt_controlhorario/custom/control_horario"
            #         }]
            #     }
            return {
                    "appConfiguration": [{
                        "key": "controlhorario",
                        "text": "Control horario",
                        "href": "/gesttare/gt_controlhorario/custom/control_horario"
                    }]
                }


        nombre_proyecto = " // Proyecto: "
        codcliente = qsatype.FLUtil.quickSqlSelect("gt_proyectos p INNER JOIN gt_tareas ta ON p.idproyecto = ta.idproyecto INNER JOIN gt_clientes c on p.idcliente = c.idcliente", "c.codcliente", "ta.idtarea = {}".format(tareaactiva))
        if codcliente:
            nombre_proyecto += codcliente + " " 
        nombre_proyecto += qsatype.FLUtil.quickSqlSelect("gt_proyectos p INNER JOIN gt_tareas ta ON p.idproyecto = ta.idproyecto", "p.nombre", "ta.idtarea = {}".format(tareaactiva))
        nombre_tarea = qsatype.FLUtil.quickSqlSelect("gt_tareas", "nombre", "idtarea = {}".format(tareaactiva))

        appinfo = {
            "data": [{
                "pk": tareaactiva,
                "idtarea": tareaactiva,
                "nombreactiva": nombre_tarea,
                "nombreproyecto": nombre_proyecto
            }],
            "layout": {
                "tareaActiva": {
                    "componente": "YBAppInfo",
                    "prefix": "appinfo",
                    "action": {
                        "key": "startstop",
                        "success": [{"slot": "refrescar"}]
                    }
                }
            },
            "acciones": {
                "startstop": {
                    "action": "legacy",
                    "iconurl" : "/static/dist/img/icons/timetrakcer.svg",
                    "serverAction": "startstop"
                }
            }
        }


        # if tengomodulo:
        #     appinfo["appConfiguration"] =  [{
        #             "key": "controlhorario",
        #             "text": "Control horario",
        #             "href": "/gesttare/gt_controlhorario/custom/control_horario"
        #         }]

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
        idc_horario = qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idusuario = {} AND horafin IS NULL".format(usuario))
        id_compania = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(usuario))
        id_plan = qsatype.FLUtil.quickSqlSelect("aqn_companies", "idplan", "idcompany = '{}'".format(id_compania)) or None
        # if not tengomodulo:
        #     return "hidden"
        if idc_horario and id_plan != 1 and id_plan != 2 and id_plan != 5:
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
