# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *


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
        if cursor.valueBuffer("codproyecto"):
            curP = qsatype.FLSqlCursor("gt_proyectos")
            curP.select(ustr("codproyecto = '", cursor.valueBuffer("codproyecto"), "'"))
            if not curP.first():
                return False
            cursor.setValueBuffer("fechainicio", curP.valueBuffer("fechainicio"))

        # tieneCoordinacion = qsatype.FLUtil.sqlSelect(u"gt_hitosproyecto", u"nombre", ustr(u"nombre = 'Coordinación' AND codproyecto = '", str(cursor.valueBuffer("codproyecto")), u"'"))

        tieneHitos = qsatype.FLUtil.sqlSelect(u"gt_hitosproyecto", u"nombre", ustr(u"codproyecto = '", str(cursor.valueBuffer("codproyecto")), u"'"))

        if cursor.valueBuffer("nombre") == None and not tieneHitos:
            cursor.setValueBuffer("nombre", "Coordinación")

        qsatype.FactoriaModulos.get('formRecordgt_hitosproyecto').iface.iniciaValoresCursor(cursor)
        return True

    def gesttare_getHitosProyecto(self, oParam):
        data = []
        if "codproyecto" not in oParam:
            return data
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_proyectos, gt_hitosproyecto")
        q.setSelect(u"h.idhito, h.nombre")
        q.setFrom(u"gt_proyectos p INNER JOIN gt_hitosproyecto h ON p.codproyecto = h.codproyecto")
        q.setWhere(u"p.codproyecto = '" + str(oParam['codproyecto']) + "' AND (UPPER(h.nombre) LIKE UPPER('%" + oParam["val"] + "%')) AND h.resuelta = false  ORDER BY h.nombre LIMIT 8")

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
        q.setFrom(u"gt_proyectos p INNER JOIN gt_hitosproyecto h ON p.codproyecto = h.codproyecto INNER JOIN gt_particproyecto pp ON p.codproyecto = pp.codproyecto")
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
        numHitos = qsatype.FLUtil.sqlSelect(u"gt_hitosproyectos", u"COUNT(idhito)", ustr(u"codproyecto = '", str(cursor.valueBuffer("codproyecto")), u"'"))
        if numHitos == 1:
            resul["status"] = 1
            resul["msg"] = "No puedes eliminar el hito"
            return resul
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
                resul["msg"] = "No se puede eliminar el hito"
                return resul
        else:
            if str(cursor.valueBuffer("idresponsable")) == str(usuario) or is_superuser:
                resul['status'] = 2
                resul['confirm'] = "¿Seguro que quieres eliminar el hito y todas sus tareas asociadas?"
            else:
                resul["status"] = 1
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
            q = qsatype.FLSqlQuery()
            q.setTablesList(u"gt_tareas")
            q.setSelect(u"idtarea")
            q.setFrom(u"gt_tareas")
            q.setWhere(u"resuelta = false AND idhito = {}".format(cursor.valueBuffer("idhito")))
            if not q.exec_():
                return False
            pendientes = q.size() or 0
            if pendientes > 0:
                response["status"] = 2
                response["confirm"] = "Al completar el hito vas a completar automáticamente todas las tareas que estén pendientes en el hito. </br></br> ¿Quieres continuar?"
                response["serverAction"] = "completar_hito"
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
        presupuestoProyecto = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"presupuesto", ustr(u"codproyecto = '", str(cursor.valueBuffer(u"codproyecto")), "'")) or 0
        sumaPresupuestos = qsatype.FLUtil.sqlSelect(u"gt_hitosproyecto", u"SUM(presupuesto)", ustr(u"codproyecto = '", str(cursor.valueBuffer(u"codproyecto")), "' AND idhito <> ", cursor.valueBuffer("idhito"), "")) or 0
        if presupuestoHito > presupuestoProyecto:
            qsatype.FLUtil.ponMsgError("El presupesto del hito es mayor al del proyecto")
            return False
        sumaPresupuestos = sumaPresupuestos + presupuestoHito

        if sumaPresupuestos > presupuestoProyecto:
            qsatype.FLUtil.ponMsgError("La suma de presupestos de los hitos es mayor que el presupuesto del proyecto")
            return False

        return True

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
