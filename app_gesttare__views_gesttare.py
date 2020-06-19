# @class_declaration interna #
from YBLEGACY import qsatype
from models.flgesttare import flgesttare_def

class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
class gesttare(interna):

    def gesttare_get_app_info(self, model, data):
        # print("entra")
        # flgesttare_def.iface.revisar_indicadores()
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
        return {"YBNavBarActions": {"pauseControlHorario": "drawIfPauseControl", "startControlHorario": "drawIfstartControl", "recordatorio":"drawIffechaAtrasada", "recordatorioCon":"drawIffechaAtrasadaCon", "recordatorioAnotar":"drawIfrecordatorioAnotar", "recordatorioAnotarCon":"drawIfrecordatorioAnotarCon", "recordatorioPlanear":"drawIfrecordatorioPlanear", "recordatorioPlanearCon":"drawIfrecordatorioPlanearCon"}}

    def gesttare_drawIfPauseControl(self, cursor):
        usuario = qsatype.FLUtil.nameUser() 
        tramoactivo = qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idusuario = {} AND horafin IS NULL".format(usuario))
        idcompany = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(usuario))
        id_plan = qsatype.FLUtil.quickSqlSelect("aqn_companies", "idplan", "idcompany = '{}'".format(idcompany)) or None
        # tengomodulo = qsatype.FLUtil.quickSqlSelect("aqn_modulescompanies", "id", "idcompany = '{}'".format(idcompany))
        # if not tengomodulo:
        #     return "hidden"
        if id_plan == 2 or id_plan == 5:
            return "hidden"
        if not tramoactivo:
            return "hidden"
        return True

    def gesttare_drawIfstartControl(self, cursor):
        usuario = qsatype.FLUtil.nameUser() 
        # idcompany = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(usuario))
        # tengomodulo = qsatype.FLUtil.quickSqlSelect("aqn_modulescompanies", "id", "idcompany = '{}'".format(idcompany))
        idc_horario = qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "idc_horario", "idusuario = {} AND horafin IS NULL".format(usuario))
        id_compania = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(usuario))
        id_plan = qsatype.FLUtil.quickSqlSelect("aqn_companies", "idplan", "idcompany = '{}'".format(id_compania)) or None
        # if not tengomodulo:
        #     return "hidden"
        if idc_horario and id_plan != 1 and id_plan != 2 and id_plan != 5:
            return "hidden"
        return True

    def gesttare_drawIffechaAtrasada(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        atrasada = qsatype.FLUtil.quickSqlSelect("gt_tareas t INNER JOIN gt_proyectos p ON t.idproyecto = p.idproyecto", "COUNT(t.idtarea)", "t.resuelta = false AND t.fechavencimiento < '{}' AND t.idusuario = '{}' AND p.archivado = false".format(str(qsatype.Date())[:10] ,usuario))
        # revisada = qsatype.FLUtil.quickSqlSelect("gt_actualizusuario", "COUNT(idactualizusuario)", "revisada = false AND idusuario = '{}' ".format(str(usuario))) 
        revisada_bandeja_fecha = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones INNER JOIN gt_actualizusuario ON gt_actualizaciones.idactualizacion = gt_actualizusuario.idactualizacion", "COUNT(gt_actualizaciones.fecha)", "gt_actualizusuario.revisada = false AND gt_actualizusuario.idusuario = '{}' AND gt_actualizaciones.fecha < CURRENT_DATE".format(str(usuario)))

        espera_sin_modificacion = qsatype.FLUtil.quickSqlSelect("gt_tareas", "COUNT(idtarea)", "codestado = 'En espera' AND resuelta = false AND idusuario = '{}' AND ultimamodificacion < CURRENT_DATE - 7".format(str(usuario)))

        # if revisada_bandeja_fecha > 0 

        if atrasada > 0 or revisada_bandeja_fecha > 0 or espera_sin_modificacion > 0:
            return "hidden"
        else:
            revisada_bandeja_hora = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones INNER JOIN gt_actualizusuario ON gt_actualizaciones.idactualizacion = gt_actualizusuario.idactualizacion", "COUNT(gt_actualizaciones.fecha)", "gt_actualizusuario.revisada = false AND gt_actualizusuario.idusuario = '{}' AND gt_actualizaciones.hora < CURRENT_TIME - TIME '03:00' AND gt_actualizaciones.tipo <> 'anotacion'".format(str(usuario)))
            if atrasada > 0 or revisada_bandeja_hora > 0 or espera_sin_modificacion > 0:
                return "hidden"
        
        # if atrasada > 0 or revisada > 0:
        #     return "hidden"
        return True

    def gesttare_drawIffechaAtrasadaCon(self, cursor):
        usuario = qsatype.FLUtil.nameUser() 
        atrasada = qsatype.FLUtil.quickSqlSelect("gt_tareas t INNER JOIN gt_proyectos p ON t.idproyecto = p.idproyecto", "COUNT(t.idtarea)", "t.resuelta = false AND t.fechavencimiento < '{}' AND t.idusuario = '{}' AND p.archivado = false".format(str(qsatype.Date())[:10] ,usuario))
        # revisada = qsatype.FLUtil.quickSqlSelect("gt_actualizusuario", "COUNT(idactualizusuario)", "revisada = false AND idusuario = '{}' ".format(str(usuario))) 
        # if atrasada == 0 and revisada == 0:
        #     return "hidden"
        revisada_bandeja_fecha = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones INNER JOIN gt_actualizusuario ON gt_actualizaciones.idactualizacion = gt_actualizusuario.idactualizacion", "COUNT(gt_actualizaciones.fecha)", "gt_actualizusuario.revisada = false AND gt_actualizusuario.idusuario = '{}' AND gt_actualizaciones.fecha < CURRENT_DATE".format(str(usuario)))

        revisada_bandeja_hora = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones INNER JOIN gt_actualizusuario ON gt_actualizaciones.idactualizacion = gt_actualizusuario.idactualizacion", "COUNT(gt_actualizaciones.fecha)", "gt_actualizusuario.revisada = false AND gt_actualizusuario.idusuario = '{}' AND gt_actualizaciones.hora < CURRENT_TIME - TIME '03:00' AND gt_actualizaciones.tipo <> 'anotacion'".format(str(usuario)))

        espera_sin_modificacion = qsatype.FLUtil.quickSqlSelect("gt_tareas", "COUNT(idtarea)", "codestado = 'En espera' AND resuelta = false AND idusuario = '{}' AND ultimamodificacion < CURRENT_DATE - 7".format(str(usuario)))

        if atrasada == 0 and revisada_bandeja_fecha == 0 and revisada_bandeja_hora == 0 and espera_sin_modificacion == 0:
            return "hidden"
        # else:
        #     revisada_bandeja_hora = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones INNER JOIN gt_actualizusuario ON gt_actualizaciones.idactualizacion = gt_actualizusuario.idactualizacion", "COUNT(gt_actualizaciones.fecha)", "gt_actualizusuario.revisada = false AND gt_actualizusuario.idusuario = '{}' AND gt_actualizaciones.hora < CURRENT_TIME - TIME '03:00'".format(str(usuario)))
        #     print(revisada_bandeja_hora)
        #     if atrasada == 0 and revisada_bandeja_hora == 0:
        #         return "hidden"
        return True

    def gesttare_drawIfrecordatorioAnotar(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        revisada_bandeja_anotacion_hora = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones INNER JOIN gt_actualizusuario ON gt_actualizaciones.idactualizacion = gt_actualizusuario.idactualizacion", "COUNT(gt_actualizaciones.fecha)", "gt_actualizusuario.revisada = false AND gt_actualizusuario.idusuario = '{}' AND gt_actualizaciones.fecha < CURRENT_DATE  AND gt_actualizaciones.tipo = 'anotacion'".format(str(usuario)))


        if revisada_bandeja_anotacion_hora > 0:
            return "hidden"

        return True

    def gesttare_drawIfrecordatorioAnotarCon(self, cursor):
        usuario = qsatype.FLUtil.nameUser() 

        revisada_bandeja_anotacion_hora = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones INNER JOIN gt_actualizusuario ON gt_actualizaciones.idactualizacion = gt_actualizusuario.idactualizacion", "COUNT(gt_actualizaciones.fecha)", "gt_actualizusuario.revisada = false AND gt_actualizusuario.idusuario = '{}' AND gt_actualizaciones.fecha < CURRENT_DATE  AND gt_actualizaciones.tipo = 'anotacion'".format(str(usuario)))

        if revisada_bandeja_anotacion_hora == 0:
            return "hidden"

        return True


    def gesttare_drawIfrecordatorioPlanear(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        tarea_sin_modificacion = qsatype.FLUtil.quickSqlSelect("gt_tareas", "COUNT(idtarea)", "fechavencimiento is null AND fechaentrega is null AND resuelta = false AND idusuario = '{}' AND ultimamodificacion < CURRENT_DATE - 30".format(str(usuario)))

        if tarea_sin_modificacion > 0:
            return "hidden"

        return True

    def gesttare_drawIfrecordatorioPlanearCon(self, cursor):
        usuario = qsatype.FLUtil.nameUser() 

        tarea_sin_modificacion = qsatype.FLUtil.quickSqlSelect("gt_tareas", "COUNT(idtarea)", "fechavencimiento is null AND fechaentrega is null AND resuelta = false AND idusuario = '{}' AND ultimamodificacion < CURRENT_DATE - 30".format(str(usuario)))

        if tarea_sin_modificacion == 0:
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

    def drawIffechaAtrasada(self, cursor):
        return self.ctx.gesttare_drawIffechaAtrasada(cursor)

    def drawIffechaAtrasadaCon(self, cursor):
        return self.ctx.gesttare_drawIffechaAtrasadaCon(cursor)

    def drawIfrecordatorioAnotar(self, cursor):
        return self.ctx.gesttare_drawIfrecordatorioAnotar(cursor)

    def drawIfrecordatorioAnotarCon(self, cursor):
        return self.ctx.gesttare_drawIfrecordatorioAnotarCon(cursor)

    def drawIfrecordatorioPlanear(self, cursor):
        return self.ctx.gesttare_drawIfrecordatorioPlanear(cursor)

    def drawIfrecordatorioPlanearCon(self, cursor):
        return self.ctx.gesttare_drawIfrecordatorioPlanearCon(cursor)


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
