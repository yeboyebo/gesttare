# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
from YBUTILS.viewREST import cacheController
import time
import datetime


class gesttare(interna):

    def gesttare_afterCommit_gt_comentarios(self, curComentario=None):
        _i = self.iface
        if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_comentarios(curComentario):
            return False
        if curComentario.modeAccess() == curComentario.Insert:
            print("gesttare_aftercommit_gt_comentarios")
            if not _i.crearActualizaciones(u"Nuevo comentario", curComentario):
                return False
        return True

    def gesttare_afterCommit_gt_tareas(self, curTarea=None):
        _i = self.iface
        actualizacion = False
        tipo = ""
        if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_tareas(curTarea):
            return False

        _i.comprobarUsuarioResponsable(curTarea)
        print("gesttare_aftercommit_gt_tareas")

        if curTarea.modeAccess() == curTarea.Edit:
            if curTarea.valueBuffer(u"codestado") != curTarea.valueBufferCopy(u"codestado"):
                actualizacion = True
                tipo = u"Cambio de estado"
            if curTarea.valueBuffer(u"fechavencimiento") != curTarea.valueBufferCopy(u"fechavencimiento"):
                print("Cambiando fecha en edit")
                actualizacion = True
                tipo = u"Cambio de fecha"
            if actualizacion:
                _i.crearActualizaciones(tipo, curTarea)

        return True

    def gesttare_afterCommit_gt_partictarea(self, curPart=None):
        _i = self.iface
        print("partictarea")
        if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_partictarea(curPart):
            return False
        # print("partictarea 2")
        if curPart.modeAccess() == curPart.Insert:
            print("gesttare_aftercommit_gt_partictarea")
            if not _i.crearActualizaciones(u"Nuevos asignados", curPart):
                return False

        return True

    def gesttare_crearActualizaciones(self, tipo, cursor=None):
        _i = self.iface
        idUsuario = qsatype.FLUtil.nameUser()
        idComentario = u""

        print("paso 4")
        qryParticipantes = qsatype.FLSqlQuery()
        qryParticipantes.setTablesList(u"gt_partictarea")
        qryParticipantes.setSelect(u"idparticipante,idusuario")
        qryParticipantes.setFrom(ustr(u"gt_partictarea"))
        qryParticipantes.setWhere(ustr(u"idtarea = ", cursor.valueBuffer(u"idtarea"), u" AND idusuario <> '", idUsuario, u"'"))
        try:
            qryParticipantes.setForwardOnly(True)
        except Exception:
            qsatype.Object()

        if not qryParticipantes.exec_():
            return False

        if qryParticipantes.size() == 0:
            return True

        print("Creando actualizaciones")
        print("tabla: ", cursor.table())

        print(datetime.date.today())

        print("paso 1")

        if cursor.table() == u"gt_comentarios":
            idComentario = cursor.valueBuffer(u"idcomentario")
            idActualizacion = qsatype.FLUtil.sqlSelect(u"gt_actualizaciones", u"idactualizacion", ustr(u"idtarea = ", cursor.valueBuffer(u"idtarea")))
            if idActualizacion:
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"idcomentario", idComentario, ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"tipo", tipo, ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"fecha", datetime.date.today(), ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"hora", time.strftime('%H:%M:%S'), ustr(u"idactualizacion = ", idActualizacion)):
                    return False
            else:
                print("insertando con hora")
                if not qsatype.FLUtil.sqlInsert(u"gt_actualizaciones", qsatype.Array([u"tipo", u"tipobjeto", u"idtarea", u"idcomentario", u"fecha", u"hora"]), qsatype.Array([tipo, u"tarea", cursor.valueBuffer(u"idtarea"), idComentario, datetime.date.today(), time.strftime('%H:%M:%S')])):
                    return False
        else:
            idActualizacion = qsatype.FLUtil.sqlSelect(u"gt_actualizaciones", u"idactualizacion", ustr(u"idtarea = ", cursor.valueBuffer(u"idtarea")))
            if idActualizacion:
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"tipo", tipo, ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"fecha", datetime.date.today(), ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"hora", time.strftime('%H:%M:%S'), ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"idcomentario", u"", ustr(u"idactualizacion = ", idActualizacion)):
                    return False
            else:
                if not qsatype.FLUtil.sqlInsert(u"gt_actualizaciones", qsatype.Array([u"tipo", u"tipobjeto", u"idtarea", u"fecha", u"hora"]), qsatype.Array([tipo, u"tarea", cursor.valueBuffer(u"idtarea"), datetime.date.today(), time.strftime('%H:%M:%S')])):
                    return False
        print("paso 2")

        if cursor.table() == u"gt_comentarios":
            idActualizacion = qsatype.FLUtil.sqlSelect(u"gt_actualizaciones", u"idactualizacion", ustr(u"idcomentario = ", idComentario))
        if (cursor.table() == u"gt_tareas") or (cursor.table() == u"gt_partictarea"):
            idActualizacion = qsatype.FLUtil.sqlSelect(u"gt_actualizaciones", u"idactualizacion", ustr(u"idtarea = ", cursor.valueBuffer(u"idtarea")))

        print("paso 3")

        if not idActualizacion:
            return False

        print("paso 5")
        while qryParticipantes.next():
            print("paso 6")
            if qsatype.FLUtil.sqlSelect(u"gt_actualizusuario", u"idactualizusuario", ustr(u"idusuario = '", qryParticipantes.value(1), u"' AND idactualizacion = ", idActualizacion)):
                continue
            if not qsatype.FLUtil.sqlInsert(u"gt_actualizusuario", qsatype.Array([u"idactualizacion", u"idusuario", u"revisada"]), qsatype.Array([idActualizacion, qryParticipantes.value(1), False])):
                return False

        print("Termina")
        return True

    def gesttare_comprobarUsuarioResponsable(self, curTarea=None):
        if curTarea.valueBufferCopy(u"idusuario") != curTarea.valueBuffer(u"idusuario"):
            if not qsatype.FLUtil.sqlSelect(u"gt_partictarea", u"idparticipante", ustr(u"idusuario = '", curTarea.valueBuffer(u"idusuario"), u"' AND idtarea = ", curTarea.valueBuffer(u"idtarea"))):
                if not qsatype.FLUtil.sqlInsert(u"gt_partictarea", qsatype.Array([u"idusuario", u"idtarea"]), qsatype.Array([curTarea.valueBuffer(u"idusuario"), curTarea.valueBuffer(u"idtarea")])):
                    return False
        print("usuario antes: ", curTarea.valueBufferCopy(u"idusuario"))
        print("usuario despues: ", curTarea.valueBuffer(u"idusuario"))
        return True

    def __init__(self, context=None):
        super().__init__(context)

    def afterCommit_gt_comentarios(self, curComentario=None):
        return self.ctx.gesttare_afterCommit_gt_comentarios(curComentario)

    def afterCommit_gt_tareas(self, curTarea=None):
        return self.ctx.gesttare_afterCommit_gt_tareas(curTarea)

    def afterCommit_gt_partictarea(self, curPart=None):
        return self.ctx.gesttare_afterCommit_gt_partictarea(curPart)

    def crearActualizaciones(self, tipo, cursor=None):
        return self.ctx.gesttare_crearActualizaciones(tipo, cursor)

    def comprobarUsuarioResponsable(self, curTarea=None):
        return self.ctx.gesttare_comprobarUsuarioResponsable(curTarea)


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


form = FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
iface = form.iface
