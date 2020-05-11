# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
from models.flgesttare import flgesttare_def
import urllib

class gesttare(interna):

    def gesttare_getDesc(self):
        return "nombre"

    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        fields = [
            {'verbose_name': 'Color responsable', 'func': 'color_responsable'},
            {'verbose_name': 'Responsable', 'func': 'field_usuario'},
            {'verbose_name': 'porcentaje', 'func': 'fun_porcentaje'},
            {'verbose_name': 'ntareas', 'func': 'fun_ntareas'},
            {"verbose_name": "color_hito", "func": "func_color_hito"},
            {"verbose_name": "presupuesto_title", "func": "func_presupuesto_title"}
        ]
        return fields

    def gesttare_get_model_info(self, model, data, ident, template, where_filter):
        # print(model, data, ident, template, where_filter)
        if template == "formRecord" and isinstance(data, list):
            if data:
                idproyecto = data[0]["idproyecto"]
                abiertas = qsatype.FLUtil.sqlSelect(u"gt_hitosproyecto", u"COUNT(idhito)", ustr(u"idproyecto = '", idproyecto, u"' AND not resuelta"))
                if abiertas == 0:
                    return {"hitosproyecto": "<div class='textRojo'>No puedes crear tareas sobre este proyecto</div>"}
        return None

    def get_model_info(self, model, data, ident, template, where_filter):
        return self.ctx.gesttare_get_model_info(model, data, ident, template, where_filter)

    def gesttare_field_usuario(self, model):
        nombre_usuario = ""
        # if hasattr(model.idresponsable, 'usuario'):
        #     print("el valor es: ",model.idresponsable.usuario)
        try:
            if not model.idusuario:
                return nombre_usuario
            nombre_usuario = "@" + model.idusuario.usuario
        except Exception:
            pass
        return nombre_usuario

        return fields

    def gesttare_color_responsable(self, model):
        if hasattr(model.idusuario, 'idusuario'):
            return "responsable"

        return ""

    def gesttare_fun_porcentaje(self, model):
        tengopermiso = flgesttare_def.iface.compruebaPermisosPlan("porcentaje_hito")
        if tengopermiso != True:
            return tengopermiso
        costeInterno = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"SUM(coste)", ustr(u"idhito = '", model.idhito, u"'"))
        if isNaN(costeInterno):
            costeInterno = 0
        presupuesto = parseFloat(model.presupuesto)
        if not presupuesto:
            return 0

        valor = ((costeInterno / presupuesto) * 100)

        if isNaN(valor):
            valor = 0
        if valor > 100:
            valor = 100
        valor = qsatype.FLUtil.roundFieldValue(valor, u"gt_proyectos", u"rentabilidad")

        return valor

    def gesttare_fun_ntareas(self, model):
        ntareas = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"count(idtarea)", ustr(u"idhito = '", str(model.idhito), u"'")) or 0
        ntareasPte = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"count(idtarea)", ustr(u"idhito = '", str(model.idhito), u"' AND resuelta is false")) or 0
        resul = ntareasPte
        resul = str(ntareasPte) + " / " + str(ntareas)
        # if (ntareas != ntareasPte):
        #     resul = str(ntareasPte) + " / " + str(ntareas)
        return resul 

    def gesttare_iniciaValoresCursor(self, cursor=None):
        usuario = qsatype.FLUtil.nameUser()
        # cursor.setValueBuffer(u"idcompany", idcompany)
        cursor.setValueBuffer("idusuario", usuario)
        if cursor.valueBuffer("idproyecto"):
            curP = qsatype.FLSqlCursor("gt_proyectos")
            curP.select(ustr("idproyecto = '", cursor.valueBuffer("idproyecto"), "'"))
            if not curP.first():
                return False
            cursor.setValueBuffer("fechainicio", curP.valueBuffer("fechainicio"))

        # tieneCoordinacion = qsatype.FLUtil.sqlSelect(u"gt_hitosproyecto", u"nombre", ustr(u"nombre = 'Coordinación' AND idproyecto = '", str(cursor.valueBuffer("idproyecto")), u"'"))

        tieneHitos = qsatype.FLUtil.sqlSelect(u"gt_hitosproyecto", u"nombre", ustr(u"idproyecto = '", str(cursor.valueBuffer("idproyecto")), u"'"))

        if cursor.valueBuffer("nombre") == None and not tieneHitos:
            cursor.setValueBuffer("nombre", "Coordinación")

        qsatype.FactoriaModulos.get('formRecordgt_hitosproyecto').iface.iniciaValoresCursor(cursor)
        return True

    def gesttare_getHitosProyecto(self, oParam):
        data = []
        if "idproyecto" not in oParam:
            return data
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_proyectos, gt_hitosproyecto")
        q.setSelect(u"h.idhito, h.nombre")
        q.setFrom(u"gt_proyectos p INNER JOIN gt_hitosproyecto h ON p.idproyecto = h.idproyecto")
        q.setWhere(u"p.idproyecto = '" + str(oParam['idproyecto']) + "' AND (UPPER(h.nombre) LIKE UPPER('%" + oParam["val"] + "%')) AND h.resuelta = false  ORDER BY h.nombre LIMIT 8")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 100:
            print("sale por aqui")
            return []

        while q.next():
            # descripcion = str(q.value(2)) + "€ " + q.value(1)
            data.append({"idhito": q.value(0), "nombre": q.value(1)})
        return data

    def gesttare_getHitosProyectosUsu(self, oParam):
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_proyectos, gt_hitosproyecto, gt_particproyecto")
        q.setSelect(u"h.idhito, h.nombre, p.nombre")
        q.setFrom(u"gt_proyectos p INNER JOIN gt_hitosproyecto h ON p.idproyecto = h.idproyecto INNER JOIN gt_particproyecto pp ON p.idproyecto = pp.idproyecto")
        q.setWhere(u"pp.idusuario = '" + qsatype.FLUtil.nameUser() + "' AND (UPPER(h.nombre) LIKE UPPER('%" + oParam["val"] + "%')) AND h.resuelta = false  ORDER BY h.nombre LIMIT 8")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 100:
            print("sale por aqui")
            return []

        while q.next():
            # descripcion = str(q.value(2)) + "€ " + q.value(1)
            data.append({"idhito": q.value(0), "nombre": q.value(1) + " // " + q.value(2)})
        return data

    def gesttare_borrar_hito(self, model, oParam, cursor):
        resul = {}
        usuario = qsatype.FLUtil.nameUser()
        is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        numHitos = qsatype.FLUtil.sqlSelect(u"gt_hitosproyecto", u"COUNT(idhito)", ustr(u"idproyecto = '", str(cursor.valueBuffer("idproyecto")), u"'"))
        if "confirmacion" in oParam and oParam["confirmacion"]:
            if str(cursor.valueBuffer("idresponsable")) == str(usuario) or is_superuser:
                cursor.setModeAccess(cursor.Del)
                cursor.refreshBuffer()
                if not cursor.commitBuffer():
                    return False
                resul["return_data"] = False
                resul["msg"] = "Hito eliminado"
                return resul
            else:
                resul["status"] = 1
                resul["resul"] = False
                resul["msg"] = "No se puede eliminar el hito"
                return resul
        elif numHitos == 1:
            resul['status'] = 2
            resul['confirm'] = "¿Seguro que quieres eliminar el hito y todas sus tareas asociadas?<br><br><i>Recuerda: Vas a eliminar el último hito del proyecto, no podrás crear tareas hasta tener un hito activo.</i>"
            return resul
        else:
            if str(cursor.valueBuffer("idresponsable")) == str(usuario) or is_superuser:
                resul['status'] = 2
                resul['confirm'] = "¿Seguro que quieres eliminar el hito y todas sus tareas asociadas?"
            else:
                resul["status"] = 1
                resul["resul"] = False
                resul["msg"] = "No puedes eliminar el hito"
                return resul
        return resul

    def gesttare_drawif_completarHito(self, cursor):
        if cursor.valueBuffer("resuelta") == True:
            return "hidden"

    def gesttare_drawif_abrirHito(self, cursor):
        if cursor.valueBuffer("resuelta") == False:
            return "hidden"

    def gesttare_completar_hito(self, model, oParam, cursor):
        response = {}
        resuelta = cursor.valueBuffer("resuelta")
        if (not oParam or "confirmacion" not in oParam) and not resuelta:
            # renegociar = qsatype.FLUtil.quickSqlSelect("gt_tareas", "COUNT(idtarea)", "resuelta = false AND fechavencimiento < '{}' AND idusuario = '{}'".format(str(qsatype.Date())[:10] ,user_name)) or 0
            hitosActivos = qsatype.FLUtil.quickSqlSelect("gt_hitosproyecto", "COUNT(idhito)", "resuelta = false AND idproyecto = '{}' and idhito <> '{}'".format(cursor.valueBuffer("idproyecto"), cursor.valueBuffer("idhito"))) or 0
            print(hitosActivos)
            q = qsatype.FLSqlQuery()
            q.setTablesList(u"gt_tareas")
            q.setSelect(u"idtarea")
            q.setFrom(u"gt_tareas")
            q.setWhere(u"resuelta = false AND idhito = {}".format(cursor.valueBuffer("idhito")))
            if not q.exec_():
                return False
            pendientes = q.size() or 0
            print(pendientes)
            if pendientes > 0:
                response["status"] = 2
                response["confirm"] = "Al completar el hito vas a completar automáticamente todas las tareas que estén pendientes en el hito."
                if hitosActivos == 0 and not resuelta:
                    response["confirm"] += "<br><br><i>Recuerda: Vas a cerrar el último hito del proyecto, no podrás crear tareas hasta tener un hito activo.</i>"
                response["confirm"] += "</br></br> ¿Quieres continuar?"
                response["serverAction"] = "completar_hito"
                # response["customButtons"] = [{"serverAction": "completar_hito","nombre": "Sí"}, {"accion": "cancel","nombre": "No"}]
                return response
            elif hitosActivos == 0 and not resuelta:
                response["status"] = 2
                response["confirm"] = "Recuerda: Vas a cerrar el último hito del proyecto, no podrás crear tareas hasta tener un hito activo."
                response["confirm"] += "</br></br> ¿Quieres continuar?"
                response["serverAction"] = "completar_hito"
                print("deberia salir por aqui???")
                # response["customButtons"] = [{"serverAction": "completar_hito","nombre": "Sí"}, {"accion": "cancel","nombre": "No"}]
                return response
        cursor.setValueBuffer("resuelta", not resuelta)

        if not cursor.commitBuffer():
            print("Ocurrió un error al actualizar el hito")
            return False

        response["resul"] = True
        if resuelta:
            response["msg"] = "Hito abierto"
        else:
            response["msg"] = "Hito completado"
        return response

    def gesttare_abrir_hito(self, model, cursor):
        response = {}
        resuelta = cursor.valueBuffer("resuelta")
        cursor.setValueBuffer("resuelta", not resuelta)

        if not cursor.commitBuffer():
            print("Ocurrió un error al actualizar el hito")
            return False

        response["resul"] = True
        if resuelta:
            response["msg"] = "Hito abierto"
        return response

    def gesttare_func_color_hito(self, model):
        if model.resuelta:
            return "hitocompletado"
        return ""

    def gesttare_func_presupuesto_title(self, model):
        costeInterno = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"SUM(coste)", ustr(u"idhito = '", model.idhito, u"'"))
        if isNaN(costeInterno):
            costeInterno = 0
        presupuesto = parseFloat(model.presupuesto)
        if not presupuesto:
            return "0€ consumidos - 0%"

        valor = ((costeInterno / presupuesto) * 100)

        if isNaN(valor):
            valor = 0

        title = str(int(costeInterno)) +"€ consumidos - " + str(int(valor)) + "%"
        return title

    def gesttare_verTarea(self, model, cursor):
        response = {}
        response["url"] = "/gesttare/gt_tareas/master"
        response["prefix"] = "gt_tareas"
        response["filter"] = '{"idhito": "' + str(cursor.valueBuffer("idhito")) + '"}'
        return response

    def gesttare_validateCursor(self, cursor):
        presupuestoHito = cursor.valueBuffer("presupuesto") or 0
        presupuestoProyecto = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"presupuesto", ustr(u"idproyecto = '", str(cursor.valueBuffer(u"idproyecto")), "'")) or 0
        sumaPresupuestos = qsatype.FLUtil.sqlSelect(u"gt_hitosproyecto", u"SUM(presupuesto)", ustr(u"idproyecto = '", str(cursor.valueBuffer(u"idproyecto")), "' AND idhito <> ", cursor.valueBuffer("idhito"), "")) or 0
        if presupuestoHito > presupuestoProyecto:
            qsatype.FLUtil.ponMsgError("El presupesto del hito es mayor al del proyecto")
            return False
        sumaPresupuestos = sumaPresupuestos + presupuestoHito

        if sumaPresupuestos > presupuestoProyecto:
            qsatype.FLUtil.ponMsgError("La suma de presupestos de los hitos es mayor que el presupuesto del proyecto")
            return False

        return True

    def gesttare_creartareahito(self, oParam, cursor):
        usuario = qsatype.FLUtil.nameUser()
        response = {}
        curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
        curProyectos.select("idusuario = '" + str(usuario) + "'")
        if not curProyectos.first():
            response["status"] = 1
            response["msg"] = "Debes participar en un proyecto para anotar tareas"
            return response
        params = ""
        if cursor.valueBuffer("idhito"):
            params += "?p_idproyecto=" + urllib.parse.quote(str(cursor.valueBuffer("idproyecto")))
            params += "&p_idhito=" + urllib.parse.quote(str(cursor.valueBuffer("idhito")))
            
        response["url"] = '/gesttare/gt_tareas/newRecord' + params
        return response

    def __init__(self, context=None):
        super().__init__(context)

    def verTarea(self, model, cursor):
        return self.ctx.gesttare_verTarea(model, cursor)

    def getHitosProyecto(self, oParam):
        return self.ctx.gesttare_getHitosProyecto(oParam)

    def getHitosProyectosUsu(self, oParam):
        return self.ctx.gesttare_getHitosProyectosUsu(oParam)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def field_usuario(self, model):
        return self.ctx.gesttare_field_usuario(model)

    def color_responsable(self, model):
        return self.ctx.gesttare_color_responsable(model)

    def creartareahito(self, oParam, cursor):
        return self.ctx.gesttare_creartareahito(oParam, cursor)

    def fun_porcentaje(self, model):
        return self.ctx.gesttare_fun_porcentaje(model)

    def fun_ntareas(self, model):
        return self.ctx.gesttare_fun_ntareas(model)

    def func_color_hito(self, model):
        return self.ctx.gesttare_func_color_hito(model)

    def func_presupuesto_title(self, model):
        return self.ctx.gesttare_func_presupuesto_title(model)

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.gesttare_iniciaValoresCursor(cursor)

    def completar_hito(self, model, oParam, cursor):
        return self.ctx.gesttare_completar_hito(model, oParam, cursor)

    def abrir_hito(self, model, cursor):
        return self.ctx.gesttare_abrir_hito(model, cursor)

    def drawif_completarHito(self, cursor):
        return self.ctx.gesttare_drawif_completarHito(cursor)

    def drawif_abrirHito(self, cursor):
        return self.ctx.gesttare_drawif_abrirHito(cursor)

    def borrar_hito(self, model, oParam, cursor):
        return self.ctx.gesttare_borrar_hito(model, oParam, cursor)

    def validateCursor(self, cursor):
        return self.ctx.gesttare_validateCursor(cursor)


# @class_declaration head #
class head(gesttare):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
