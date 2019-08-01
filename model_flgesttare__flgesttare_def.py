# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
import time
from models.flgesttare.gt_proyectos import gt_proyectos as proyectos
import datetime


class gesttare(interna):

    def gesttare_afterCommit_gt_comentarios(self, curComentario=None):
        _i = self.iface
        if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_comentarios(curComentario):
            return False
        if curComentario.modeAccess() == curComentario.Insert:
            nombreTarea = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"nombre", ustr(u"idtarea = ", curComentario.valueBuffer(u"idtarea"), ""))
            if not _i.crearActualizaciones(u"Nuevo comentario a " + nombreTarea.replace("'", ""), curComentario):
                return False
        return True

    def gesttare_afterCommit_gt_proyectos(self, curProyecto=None):
        _i = self.iface
        # if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_proyectos(curProyecto):
        #     return False

        print("gesttare_aftercommit_gt_proyectos")
        if not _i.comprobarUsuarioResponsableProyecto(curProyecto):
            return False

        return True

    def gesttare_afterCommit_gt_tareas(self, curTarea=None):
        _i = self.iface
        # if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_tareas(curTarea):
        #     return False

        _i.comprobarUsuarioResponsable(curTarea)
        # print("gesttare_aftercommit_gt_tareas")

        _i.comprobarActualizacionesTareas(curTarea)

        if not _i.controlCosteProyecto(curTarea):
            return False

        return True

    def gesttare_controlCosteProyecto(self, curT=None):
        _i = self.iface

        if curT.modeAccess() == curT.Edit:
            if curT.valueBuffer(u"coste") != curT.valueBufferCopy(u"coste"):
                if not _i.totalizaCostesProyecto(curT.valueBuffer(u"codproyecto")):
                    return False

        return True

    def gesttare_totalizaCostesProyecto(self, codProyecto=None):
        print("totalizar costes proyecto")
        _i = self.iface
        curP = qsatype.FLSqlCursor(u"gt_proyectos")
        curP.select(ustr(u"codproyecto = '", codProyecto, u"'"))
        if not curP.first():
            return False
        curP.setModeAccess(curP.Edit)
        curP.refreshBuffer()
        curP.setValueBuffer(u"costeinterno", proyectos.getIface().commonCalculateField(u"costeinterno", curP))
        curP.setValueBuffer(u"costetotal", proyectos.getIface().commonCalculateField(u"costetotal", curP))
        curP.setValueBuffer(u"rentabilidad", proyectos.getIface().commonCalculateField(u"rentabilidad", curP))
        if not curP.commitBuffer():
            return False
        return True

    def gesttare_afterCommit_gt_partictarea(self, curPart=None):
        _i = self.iface
        if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_partictarea(curPart):
            return False
        # print("partictarea 2")
        if curPart.modeAccess() == curPart.Insert:
            nombreTarea = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"nombre", ustr(u"idtarea = ", curPart.valueBuffer(u"idtarea"), ""))
            if not _i.crearActualizaciones(u"Añadido participante tarea " + nombreTarea.replace("'", ""), curPart):
                return False

        return True

    def gesttare_afterCommit_gt_particproyecto(self, curPart=None):
        _i = self.iface
        # if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_particproyecto(curPart):
        #     return False

        if curPart.modeAccess() == curPart.Del:
            if not _i.desasignarTareasProyecto(curPart):
                return False

            if not _i.eliminarNotificacionesProyecto(curPart):
                return False

            # count = qsatype.FLUtil.sqlSelect(u"gt_particproyecto", u"count(*)", ustr(u"codproyecto = '", str(curPart.valueBuffer(u"codproyecto")), u"'"))
            # if count == 0:
            #     return False

        if curPart.modeAccess() == curPart.Insert:
            nombreProyecto = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"nombre", ustr(u"codproyecto = '", str(curPart.valueBuffer(u"codproyecto")), "'"))
            if not _i.crearActualizaciones(u"Añadido participante en proyecto " + nombreProyecto.replace("'", ""), curPart):
                return False

        return True

    def gesttare_eliminarNotificacionesProyecto(self, curPart):
        # qsatype.FLSqlQuery().execSql("DELETE FROM gt_partictarea where idusuario = " + str(curPart.valueBuffer("idusuario")) + " AND idtarea IN (SELECT idtarea from gt_tareas where codproyecto = '" + curPart.valueBuffer("codproyecto") + "')")
        return True

    def gesttare_desasignarTareasProyecto(self, curPart):
        qsatype.FLSqlQuery().execSql("DELETE FROM gt_partictarea where idusuario = " + str(curPart.valueBuffer("idusuario")) + " AND idtarea IN (SELECT idtarea from gt_tareas where codproyecto = '" + curPart.valueBuffer("codproyecto") + "')")
        return True

    def gesttare_crearActualizaciones(self, tipo, cursor=None):
        # _i = self.iface
        idUsuario = qsatype.FLUtil.nameUser()
        idComentario = u""
        if cursor.table() == "gt_comentarios" or cursor.table() == "gt_partictarea":
            qryParticipantes = qsatype.FLSqlQuery()
            qryParticipantes.setTablesList(u"gt_partictarea")
            qryParticipantes.setSelect(u"idparticipante,idusuario")
            qryParticipantes.setFrom(ustr(u"gt_partictarea"))
            qryParticipantes.setWhere("idtarea = {} AND idusuario <> {}".format(cursor.valueBuffer(u"idtarea"), idUsuario))

            try:
                qryParticipantes.setForwardOnly(True)
            except Exception:
                qsatype.Object()

            if not qryParticipantes.exec_():
                return False

            if qryParticipantes.size() == 0:
                return True

        if cursor.table() == u"gt_comentarios":
            idComentario = cursor.valueBuffer(u"idcomentario")
            idActualizacion = qsatype.FLUtil.sqlSelect(u"gt_actualizaciones", u"idactualizacion", "idtarea = '{}' AND tipo = '{}'".format(cursor.valueBuffer(u"idtarea"), tipo))
            if idActualizacion:
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"idcomentario", idComentario, ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"tipo", tipo, ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"fecha", datetime.date.today(), ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"hora", time.strftime('%H:%M:%S'), ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"idusuarioorigen", idUsuario, ustr(u"idactualizacion = ", idActualizacion)):
                    return False
            else:
                print("insertando con hora")
                # if not qsatype.FLUtil.sqlInsert(u"gt_actualizaciones", qsatype.Array([u"tipo", u"tipobjeto", u"idtarea", u"idcomentario", u"fecha", u"hora", u"idusuarioorigen"]), qsatype.Array([tipo, u"comentario", cursor.valueBuffer(u"idtarea"), idComentario, datetime.date.today(), time.strftime('%H:%M:%S'), idUsuario])):
                #     return False
                curActualiz = qsatype.FLSqlCursor(u"gt_actualizaciones")
                curActualiz.setModeAccess(curActualiz.Insert)
                curActualiz.refreshBuffer()
                curActualiz.setValueBuffer(u"tipo", tipo)
                curActualiz.setValueBuffer(u"tipobjeto", "comentario")
                curActualiz.setValueBuffer(u"idtarea", cursor.valueBuffer(u"idtarea"))
                curActualiz.setValueBuffer(u"idcomentario", idComentario)
                curActualiz.setValueBuffer(u"fecha", datetime.date.today())
                curActualiz.setValueBuffer(u"hora", time.strftime('%H:%M:%S'))
                curActualiz.setValueBuffer(u"idusuarioorigen", idUsuario)
                if not curActualiz.commitBuffer():
                    print("algo salio mal")
                    return False
        elif cursor.table() == u"gt_particproyecto":
            idActualizacion = qsatype.FLUtil.sqlSelect(u"gt_actualizaciones", u"idactualizacion", "idobjeto = '{}' AND tipo = '{}'".format(str(cursor.valueBuffer(u"codproyecto")), tipo))
            if idActualizacion:
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"tipo", tipo, ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"fecha", datetime.date.today(), ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"hora", time.strftime('%H:%M:%S'), ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"idusuarioorigen", idUsuario, ustr(u"idactualizacion = ", idActualizacion)):
                    return False
            else:
                if not qsatype.FLUtil.sqlInsert(u"gt_actualizaciones", qsatype.Array([u"tipo", u"tipobjeto", u"idobjeto", u"fecha", u"hora", "idusuarioorigen"]), qsatype.Array([tipo, u"proyecto", str(cursor.valueBuffer(u"codproyecto")), datetime.date.today(), time.strftime('%H:%M:%S'), idUsuario])):
                    return False
                idActualizacion = qsatype.FLUtil.sqlSelect(u"gt_actualizaciones", u"idactualizacion", "idobjeto = '{}' AND tipo = '{}'".format(str(cursor.valueBuffer(u"codproyecto")), tipo))
                if not qsatype.FLUtil.sqlInsert(u"gt_actualizusuario", qsatype.Array([u"idactualizacion", u"idusuario", u"revisada"]), qsatype.Array([idActualizacion, cursor.valueBuffer("idusuario"), False])):
                    return False
        else:
            idActualizacion = qsatype.FLUtil.sqlSelect(u"gt_actualizaciones", u"idactualizacion", "idtarea = '{}' AND tipo = '{}'".format(cursor.valueBuffer(u"idtarea"), tipo))
            if idActualizacion:
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"tipo", tipo, ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"fecha", datetime.date.today(), ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"hora", time.strftime('%H:%M:%S'), ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"idcomentario", u"", ustr(u"idactualizacion = ", idActualizacion)):
                    return False
                if not qsatype.FLUtil.sqlUpdate(u"gt_actualizaciones", u"idusuarioorigen", idUsuario, ustr(u"idactualizacion = ", idActualizacion)):
                    return False
            else:
                if not qsatype.FLUtil.sqlInsert(u"gt_actualizaciones", qsatype.Array([u"tipo", u"tipobjeto", u"idtarea", u"fecha", u"hora", "idusuarioorigen"]), qsatype.Array([tipo, u"tarea", cursor.valueBuffer(u"idtarea"), datetime.date.today(), time.strftime('%H:%M:%S'), idUsuario])):
                    return False

        if cursor.table() == u"gt_comentarios" and not idActualizacion:
            idActualizacion = curActualiz.valueBuffer("idactualizacion")
        if (cursor.table() == u"gt_tareas") or (cursor.table() == u"gt_partictarea"):
            idActualizacion = qsatype.FLUtil.sqlSelect(u"gt_actualizaciones", u"idactualizacion", "idtarea = '{}' AND tipo = '{}'".format(cursor.valueBuffer(u"idtarea"), tipo))

        if not idActualizacion:
            print("sale por algun false?")
            return False

        if cursor.table() == "gt_comentarios" or cursor.table() == "gt_partictarea":

            while qryParticipantes.next():
                if qsatype.FLUtil.sqlSelect(u"gt_actualizusuario", u"idactualizusuario", ustr(u"idusuario = ", qryParticipantes.value(1), u" AND idactualizacion = ", idActualizacion)):
                    continue
                if not qsatype.FLUtil.sqlInsert(u"gt_actualizusuario", qsatype.Array([u"idactualizacion", u"idusuario", u"revisada"]), qsatype.Array([idActualizacion, qryParticipantes.value(1), False])):
                    return False

        print("Termina")
        return True

    def gesttare_comprobarUsuarioResponsableProyecto(self, curProyecto):
        if curProyecto.modeAccess() == curProyecto.Insert:
            idUsuario = str(qsatype.FLUtil.nameUser())
            if not qsatype.FLUtil.sqlInsert(u"gt_particproyecto", qsatype.Array([u"idusuario", u"codproyecto"]), qsatype.Array([idUsuario, curProyecto.valueBuffer(u"codproyecto")])):
                return False
        return True

    def gesttare_comprobarUsuarioResponsable(self, curTarea=None):
        if curTarea.valueBufferCopy(u"idusuario") != curTarea.valueBuffer(u"idusuario") or (curTarea.modeAccess() == curTarea.Insert and curTarea.valueBuffer(u"idusuario")):
            if not qsatype.FLUtil.sqlSelect(u"gt_partictarea", u"idparticipante", ustr(u"idusuario = ", curTarea.valueBuffer(u"idusuario"), u" AND idtarea = ", curTarea.valueBuffer(u"idtarea"))):
                if not qsatype.FLUtil.sqlInsert(u"gt_partictarea", qsatype.Array([u"idusuario", u"idtarea"]), qsatype.Array([curTarea.valueBuffer(u"idusuario"), curTarea.valueBuffer(u"idtarea")])):
                    return False
        return True

    def gesttare_comprobarActualizacionesTareas(self, curTarea=None):
        _i = self.iface
        # actualizacion = False
        tipo = ""
        if curTarea.modeAccess() == curTarea.Edit:
            # if curTarea.valueBuffer(u"codestado") != curTarea.valueBufferCopy(u"codestado"):
            #     actualizacion = True
            #     tipo = u"Cambio de estado"
            if curTarea.valueBuffer(u"idusuario") != curTarea.valueBufferCopy(u"idusuario"):
                # actualizacion = True
                tipo = u"Cambio de responsable"
                _i.crearActualizaciones(tipo, curTarea)
            # if curTarea.valueBuffer(u"fechavencimiento") != curTarea.valueBufferCopy(u"fechavencimiento"):
            #     # actualizacion = True
            #     tipo = u"Cambio de fecha"
            #     print("actualizamos fecha??")
            #     _i.crearActualizaciones(tipo, curTarea)
            # if actualizacion:
            #     _i.crearActualizaciones(tipo, curTarea)
        return True

    def gesttare_afterCommit_gt_timetracking(self, cursor):
        _i = self.iface
        if not _i.controlCostesTimeTracking(cursor):
            return False
        return True

    def gesttare_controlCostesTimeTracking(self, cursor=None):
        _i = self.iface
        if cursor.modeAccess() == cursor.Insert or cursor.modeAccess() == cursor.Del:
            if cursor.valueBuffer(u"totaltiempo") != 0 or cursor.valueBuffer(u"coste") != 0:
                if not _i.totalizaCostesTarea(cursor.valueBuffer(u"idtarea")):
                    return False
        else:
            if cursor.modeAccess() == cursor.Edit:
                if cursor.valueBuffer(u"totaltiempo") != cursor.valueBufferCopy(u"totaltiempo") or cursor.valueBuffer(u"coste") != cursor.valueBufferCopy(u"coste"):
                    if not _i.totalizaCostesTarea(cursor.valueBuffer(u"idtarea")):
                        return False

        return True

    def gestttare_totalizaCostesTarea(self, idTarea):
        _i = self.iface
        curT = qsatype.FLSqlCursor(u"gt_tareas")
        curT.select(ustr(u"idtarea = ", idTarea))
        if not curT.first():
            return False
        curT.setModeAccess(curT.Edit)
        curT.refreshBuffer()
        curT.setValueBuffer(u"coste", _i.calcula_costetiempo("tarea", curT))
        if not curT.commitBuffer():
            return False
        return True

    def gesttare_calcula_costetiempo(self, tipo, cursor):
        valor = 0
        _i = self.iface
        if tipo == "tarea":
            valor = qsatype.FLUtil.sqlSelect(u"gt_timetracking", u"SUM(coste)", ustr(u"idtarea = ", cursor.valueBuffer(u"idtarea")))
            if isNaN(valor):
                valor = 0
            valor = qsatype.FLUtil.roundFieldValue(valor, u"gt_timetracking", u"coste")

        if tipo == "timetracking":
            costehora = cursor.valueBuffer(u"costehora")
            if not costehora:
                costehora = qsatype.FLUtil.sqlSelect(u"aqn_user", u"costehora", ustr(u"idusuario = ", cursor.valueBuffer(u"idusuario"))) or 0
            hdedicadas = _i.time_to_hours(cursor.valueBuffer("totaltiempo"))
            valor = costehora * hdedicadas
            valor = qsatype.FLUtil.roundFieldValue(valor, u"gt_timetracking", u"coste")
        return valor

    def gesttare_time_to_hours(self, time):
        _i = self.iface
        hdedicadas = _i.time_to_seconds(time)
        return hdedicadas / 3600

    def gesttare_time_to_seconds(self, time):
        seconds = 0
        a_time = time.split(":")

        if len(a_time) > 0:
            seconds = seconds + int(a_time[0]) * 3600
        if len(a_time) > 1:
            seconds = seconds + int(a_time[1]) * 60
        if len(a_time) > 2:
            seconds = seconds + int(a_time[2])

        return seconds

    def gesttare_beforeCommit_gt_controlhorario(self, cursor=None):
        _i = self.iface

        if not cursor.valueBuffer("idc_diario"):
            now = str(qsatype.Date())
            fecha = now[:10]
            hora = cursor.valueBuffer("horainicio")
            user_name = cursor.valueBuffer("idusuario")

            idc_diario = qsatype.FLUtil().quickSqlSelect("gt_controldiario", "idc_diario", "idusuario = '{}' AND fecha = '{}'".format(user_name, fecha))

            if not idc_diario:
                if not qsatype.FLUtil().sqlInsert("gt_controldiario", ["fecha", "horaentrada", "horasextra", "idusuario"], [fecha, hora, "00:00:00", user_name]):
                    print("Error al crear el registro diario")
                    return False

                idc_diario = qsatype.FLUtil().quickSqlSelect("gt_controldiario", "idc_diario", "idusuario = '{}' AND fecha = '{}'".format(user_name, fecha))

            cursor.setValueBuffer("idc_diario", idc_diario)

        cursor.setValueBuffer("totaltiempo", self.iface.calcula_totaltiempo_horario(cursor))

        return True

    def gesttare_beforeCommit_gt_controldiario(self, cursor=None):
        _i = self.iface

        if cursor.modeAccess() != cursor.Insert:
            return True

        fecha = cursor.valueBuffer("fecha")
        year = fecha[:4]
        month = fecha[5:7]
        user_name = cursor.valueBuffer("idusuario")

        idc_mensual = qsatype.FLUtil().quickSqlSelect("gt_controlmensual", "idc_mensual", "idusuario = '{}' AND mes = '{}' AND anyo = '{}'".format(user_name, month, year))

        if not idc_mensual:
            if not qsatype.FLUtil().sqlInsert("gt_controlmensual", ["mes", "anyo", "idusuario"], [month, year, user_name]):
                print("Error al crear el registro mensual")
                return False

            idc_mensual = qsatype.FLUtil().quickSqlSelect("gt_controlmensual", "idc_mensual", "idusuario = '{}' AND mes = '{}' AND anyo = '{}'".format(user_name, month, year))

        cursor.setValueBuffer("idc_mensual", idc_mensual)

        return True

    def gesttare_afterCommit_gt_controlhorario(self, cursor=None):
        _i = self.iface

        idc_diario = cursor.valueBuffer("idc_diario")

        cur_diario = qsatype.FLSqlCursor("gt_controldiario")
        cur_diario.select("idc_diario = {}".format(idc_diario))

        if not cur_diario.first():
            print("No se encontró el registro diario")
            return False

        cur_diario.setModeAccess(cur_diario.Edit)
        cur_diario.refreshBuffer()
        totaltiempo = self.iface.calcula_totaltiempo_diario(idc_diario)
        cur_diario.setValueBuffer("horaentrada", str(self.iface.calcula_horaentrada(idc_diario)))
        cur_diario.setValueBuffer("horasalida", str(self.iface.calcula_horasalida(idc_diario)))
        cur_diario.setValueBuffer("totaltiempo", str(totaltiempo))
        cur_diario.setValueBuffer("horasordinarias", str(self.iface.calcula_horasordinarias_diario(cur_diario)))

        if not cur_diario.commitBuffer():
            print("Ocurrió un error al actualizar el registro diario")
            return False

        return True

    def gesttare_afterCommit_gt_controldiario(self, cursor=None):
        _i = self.iface

        idc_mensual = cursor.valueBuffer("idc_mensual")

        cur_mensual = qsatype.FLSqlCursor("gt_controlmensual")
        cur_mensual.select("idc_mensual = {}".format(idc_mensual))

        if not cur_mensual.first():
            print("No se encontró el registro mensual")
            return False

        cur_mensual.setModeAccess(cur_mensual.Edit)
        cur_mensual.refreshBuffer()

        cur_mensual.setValueBuffer("totaltiempo", str(self.iface.calcula_totaltiempo_mensual(idc_mensual)))
        cur_mensual.setValueBuffer("horasextra", str(self.iface.calcula_horasextra_mensual(idc_mensual)))
        cur_mensual.setValueBuffer("horasordinarias", str(self.iface.calcula_horasordinarias_diario(cur_mensual)))

        if not cur_mensual.commitBuffer():
            print("Ocurrió un error al actualizar el registro mensual")
            return False

        return True

    def gesttare_calcula_totaltiempo_horario(self, cursor):
        if not cursor.valueBuffer("horainicio") or not cursor.valueBuffer("horafin"):
            return None

        formato = "%H:%M:%S"
        horainicio = str(cursor.valueBuffer("horainicio"))
        if len(horainicio) == 5:
            horainicio += ":00"
        horafin = str(cursor.valueBuffer("horafin"))
        if len(horafin) == 5:
            horafin += ":00"
        hfin = datetime.datetime.strptime(horafin, formato)
        hinicio = datetime.datetime.strptime(horainicio, formato)
        totaltiempo = hfin - hinicio
        totaltiempo = str(totaltiempo)
        if len(totaltiempo) < 8:
            totaltiempo = "0" + totaltiempo
        if len(totaltiempo) > 8:
            totaltiempo = totaltiempo[8:]
        return totaltiempo

    def gesttare_calcula_totaltiempo_diario(self, idc_diario):
        totaltiempo = str(qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "SUM(totaltiempo)", "idc_diario = {}".format(idc_diario))) or "00:00:00"
        if not totaltiempo or totaltiempo == "None":
            return "00:00:00"
        if len(totaltiempo) < 8:
            totaltiempo = "0" + totaltiempo
        if len(totaltiempo) > 8:
            totaltiempo = totaltiempo[8:]
        return totaltiempo

    def gesttare_calcula_horasordinarias_diario(self, cur_diario):
        if not cur_diario.valueBuffer("totaltiempo") or not cur_diario.valueBuffer("horasextra") or cur_diario.valueBuffer("totaltiempo") == "None" or cur_diario.valueBuffer("horasextra") == "None":
            return "00:00:00"

        formato = "%H:%M:%S"
        totaltiempo = str(cur_diario.valueBuffer("totaltiempo"))
        if len(totaltiempo) == 5:
            totaltiempo += ":00"
        horasextra = str(cur_diario.valueBuffer("horasextra"))
        if len(horasextra) == 5:
            horasextra += ":00"
        horasextra = datetime.datetime.strptime(horasextra, formato)
        totaltiempo = datetime.datetime.strptime(totaltiempo, formato)
        horasordinarias = totaltiempo - horasextra
        horasordinarias = str(horasordinarias)
        if len(horasordinarias) < 8:
            horasordinarias = "0" + horasordinarias
        if len(horasordinarias) > 8:
            horasordinarias = horasordinarias[8:]
        return horasordinarias

    def gesttare_calcula_horaentrada(self, idc_diario):
        return qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "MIN(horainicio)", "idc_diario = {}".format(idc_diario)) or "00:00:00"

    def gesttare_calcula_horasalida(self, idc_diario):
        return qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "MAX(horafin)", "idc_diario = {}".format(idc_diario)) or "00:00:00"

    def gesttare_calcula_totaltiempo_mensual(self, idc_mensual):
        return qsatype.FLUtil().quickSqlSelect("gt_controldiario", "SUM(totaltiempo)", "idc_mensual = {}".format(idc_mensual)) or "00:00:00"

    def gesttare_calcula_horasextra_mensual(self, idc_mensual):
        return qsatype.FLUtil().quickSqlSelect("gt_controldiario", "SUM(horasextra)", "idc_mensual = {}".format(idc_mensual)) or "00:00:00"

    def gesttare_seconds_to_time(self, seconds, total=False, all_in_hours=False):
        if not seconds:
            if total:
                seconds = 0
            else:
                return ""

        minutes = seconds // 60
        seconds = int(seconds % 60)
        hours = int(minutes // 60)
        minutes = int(minutes % 60)

        days = None
        years = None

        if not all_in_hours:
            days = hours // 24
            hours = int(hours % 24)
            years = days // 365
            days = int(days % 365)

        seconds = str(seconds) if seconds >= 10 else "0{}".format(seconds)
        minutes = str(minutes) if minutes >= 10 else "0{}".format(minutes)
        hours = str(hours) if hours >= 10 else "0{}".format(hours)

        if total:
            years = "" if not years else "{} años, ".format(years)
            days = "" if not days else "{} días, ".format(days)
            return "{}{}{}:{}:{}".format(years, days, hours, minutes, seconds)
        else:
            return "{}:{}:{}".format(hours, minutes, seconds)

    def __init__(self, context=None):
        super().__init__(context)

    def afterCommit_gt_comentarios(self, curComentario=None):
        return self.ctx.gesttare_afterCommit_gt_comentarios(curComentario)

    def afterCommit_gt_tareas(self, curTarea=None):
        return self.ctx.gesttare_afterCommit_gt_tareas(curTarea)

    def afterCommit_gt_timetracking(self, cursor=None):
        return self.ctx.gesttare_afterCommit_gt_timetracking(cursor)

    def afterCommit_gt_partictarea(self, curPart=None):
        return self.ctx.gesttare_afterCommit_gt_partictarea(curPart)

    def afterCommit_gt_particproyecto(self, curPart=None):
        return self.ctx.gesttare_afterCommit_gt_particproyecto(curPart)

    def crearActualizaciones(self, tipo, cursor=None):
        return self.ctx.gesttare_crearActualizaciones(tipo, cursor)

    def comprobarUsuarioResponsable(self, curTarea=None):
        return self.ctx.gesttare_comprobarUsuarioResponsable(curTarea)

    def comprobarActualizacionesTareas(self, curTarea=None):
        return self.ctx.gesttare_comprobarActualizacionesTareas(curTarea)

    def afterCommit_gt_proyectos(self, curProyecto=None):
        return self.ctx.gesttare_afterCommit_gt_proyectos(curProyecto)

    def comprobarUsuarioResponsableProyecto(self, curProyecto=None):
        return self.ctx.gesttare_comprobarUsuarioResponsableProyecto(curProyecto)

    def calcula_costetiempo(self, tipo, cursor):
        return self.ctx.gesttare_calcula_costetiempo(tipo, cursor)

    def controlCostesTimeTracking(self, cursor):
        return self.ctx.gesttare_controlCostesTimeTracking(cursor)

    def totalizaCostesTarea(self, idTarea):
        return self.ctx.gestttare_totalizaCostesTarea(idTarea)

    def time_to_hours(self, time):
        return self.ctx.gesttare_time_to_hours(time)

    def time_to_seconds(self, time):
        return self.ctx.gesttare_time_to_seconds(time)

    def controlCosteProyecto(self, curT):
        return self.ctx.gesttare_controlCosteProyecto(curT)

    def totalizaCostesProyecto(self, codProyecto):
        return self.ctx.gesttare_totalizaCostesProyecto(codProyecto)

    def desasignarTareasProyecto(self, curPart):
        return self.ctx.gesttare_desasignarTareasProyecto(curPart)

    def eliminarNotificacionesProyecto(self, curPart):
        return self.ctx.gesttare_eliminarNotificacionesProyecto(curPart)

    def beforeCommit_gt_controlhorario(self, cursor=None):
        return self.ctx.gesttare_beforeCommit_gt_controlhorario(cursor)

    def beforeCommit_gt_controldiario(self, cursor=None):
        return self.ctx.gesttare_beforeCommit_gt_controldiario(cursor)

    def afterCommit_gt_controlhorario(self, cursor=None):
        return self.ctx.gesttare_afterCommit_gt_controlhorario(cursor)

    def afterCommit_gt_controldiario(self, cursor=None):
        return self.ctx.gesttare_afterCommit_gt_controldiario(cursor)

    def calcula_totaltiempo_horario(self, cursor):
        return self.ctx.gesttare_calcula_totaltiempo_horario(cursor)

    def calcula_totaltiempo_diario(self, idc_diario):
        return self.ctx.gesttare_calcula_totaltiempo_diario(idc_diario)

    def calcula_horasordinarias_diario(self, cur_diario):
        return self.ctx.gesttare_calcula_horasordinarias_diario(cur_diario)

    def calcula_horaentrada(self, idc_diario):
        return self.ctx.gesttare_calcula_horaentrada(idc_diario)

    def calcula_horasalida(self, idc_diario):
        return self.ctx.gesttare_calcula_horasalida(idc_diario)

    def calcula_totaltiempo_mensual(self, idc_mensual):
        return self.ctx.gesttare_calcula_totaltiempo_mensual(idc_mensual)

    def calcula_horasextra_mensual(self, idc_mensual):
        return self.ctx.gesttare_calcula_horasextra_mensual(idc_mensual)

    def seconds_to_time(self, seconds, total=False, all_in_hours=False):
        return self.ctx.gesttare_seconds_to_time(seconds, total, all_in_hours)


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
