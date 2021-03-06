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
from models.flgesttare.gt_tareas import gt_tareas as tareas
import datetime
from YBUTILS.APIQSA import APIQSA


class gesttare(interna):

    def gesttare_afterCommit_gt_comentarios(self, curComentario):
        _i = self.iface
        if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_comentarios(curComentario):
            return False
        if curComentario.modeAccess() == curComentario.Insert:
            if not qsatype.FLUtil.sqlSelect(u"gt_partictarea", u"idparticipante", ustr(u"idusuario = ", curComentario.valueBuffer(u"idusuario"), u" AND idtarea = ", curComentario.valueBuffer(u"idtarea"))):
                # print("falla al añadir como participante???")
                if not qsatype.FLUtil.sqlInsert(u"gt_partictarea", qsatype.Array([u"idusuario", u"idtarea"]), qsatype.Array([curComentario.valueBuffer(u"idusuario"), curComentario.valueBuffer(u"idtarea")])):
                    return False
            _i.actualizarModificacion(curComentario.valueBuffer(u"idtarea"))
            # nombreTarea = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"nombre", ustr(u"idtarea = ", curComentario.valueBuffer(u"idtarea"), ""))
            _i.compruebaNotificacion("comentario", curComentario)
            
            # if not _i.crearActualizaciones(u"Nuevo comentario a " + nombreTarea.replace("'", ""), curComentario):
            #     return False
        return True

    def gesttare_afterCommit_gt_proyectos(self, curProyecto):
        _i = self.iface
        if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_proyectos(curProyecto):
            return False

        # if curProyecto.modeAccess() == curProyecto.Insert:
        #     if not _i.crearHitoInicial(curProyecto):
        #         return False

        # if not _i.comprobarUsuarioResponsableProyecto(curProyecto):
        #     return False

        if not _i.comprobarClienteProyecto(curProyecto):
            return False

        return True

    def gesttare_beforeCommit_gt_proyectos(self, curProyecto):
        _i = self.iface

        if curProyecto.modeAccess() == curProyecto.Del:
            _i.compruebaNotificacion("delproyecto", curProyecto)

        elif curProyecto.modeAccess() != curProyecto.Insert:
            if not _i.comprobarNotificacionesProyecto(curProyecto):
                return False

        return True

    def gesttare_beforeCommit_gt_hitosproyecto(self, curHito):
        _i = self.iface

        # if curHito.modeAccess() == curHito.Insert:
        #     if curHito.valueBuffer("idproyecto"):
        #         fechainicio = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"fechainicio", ustr(u"idproyecto = '", str(curHito.valueBuffer(u"idproyecto")), "'"))
        #         if fechainicio:
        #             curHito.setValueBuffer("fechainicio", fechainicio)

        return True

    def gesttare_afterCommit_gt_hitosproyecto(self, curHito):
        _i = self.iface

        if curHito.modeAccess() == curHito.Insert:
            if not _i.crearHitoInicial(curHito):
                return False

        if curHito.modeAccess() == curHito.Edit:
            if curHito.valueBuffer("resuelta") == True and (curHito.valueBuffer(u"resuelta") != curHito.valueBufferCopy(u"resuelta")):
                _i.completarTareasHito(curHito)
        if curHito.modeAccess() == curHito.Del:
            # print("notificamos deltarea")
            _i.borrarTareasHito(curHito)
        return True

    def gesttare_beforeCommit_gt_tareas(self, curTarea):
        _i = self.iface
        if curTarea.modeAccess() == curTarea.Del:
            # print("notificamos deltarea")
            _i.compruebaNotificacion("deltarea", curTarea)

        if curTarea.modeAccess() == curTarea.Edit:
            _i.controlFechaModTarea(curTarea)
            idUsuario = qsatype.FLUtil.nameUser()
            if curTarea.valueBuffer("resuelta"):
                qsatype.FLSqlQuery().execSql("DELETE FROM gt_actualizusuario where idusuario = " + str(idUsuario) + " AND idactualizacion IN (SELECT idactualizacion from gt_actualizaciones where tipobjeto = 'gt_tarea' AND idobjeto = '" + str(curTarea.valueBuffer("idtarea")) + "')")
        return True

    def gesttare_afterCommit_gt_tareas(self, curTarea):
        _i = self.iface
        # if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_tareas(curTarea):
        #     return False

        _i.comprobarUsuarioResponsable(curTarea)
        # print("gesttare_aftercommit_gt_tareas")

        _i.comprobarActualizacionesTareas(curTarea)

        _i.comprobarClienteTarea(curTarea)

        if not _i.controlCosteProyecto(curTarea):
            return False

        if curTarea.modeAccess() == curTarea.Edit:
            if curTarea.valueBuffer("idusuario"):
                if not _i.comprobarUsuarioParticProyecto(curTarea):
                    qsatype.FLUtil.ponMsgError(qsatype.FLUtil.translate(u"El responsable no participa en el proyecto"))

                    return False

            partic_tarea = qsatype.FLSqlCursor(u"gt_partictarea")
            partic_tarea.select(u"idtarea = " + str(curTarea.valueBuffer("idtarea")))
            while partic_tarea.next():
                if not _i.comprobarUsuarioParticProyectoTarea(partic_tarea.valueBuffer("idusuario"), curTarea.valueBuffer("idproyecto")):
                    partic_tarea.setModeAccess(partic_tarea.Del)
                    partic_tarea.refreshBuffer()
                    if not partic_tarea.commitBuffer():
                        return False

        if curTarea.modeAccess() == curTarea.Insert:
            params = {
                'clave': curTarea.valueBuffer("idactualizacion"),
                'idtarea': curTarea.valueBuffer("idtarea")
            }
            clave = qsatype.FLUtil.sqlSelect("gd_objetosdoc", "clave", "clave = '{}'".format(curTarea.valueBuffer("idactualizacion")))
            if clave:
                usuario = qsatype.FLUtil.nameUser()
                APIQSA.entry_point('post', "gd_objetosdoc", usuario, params, "delete_objetosdoc")

        return True
    def gesttare_controlCosteProyecto(self, curT):
        _i = self.iface

        if curT.modeAccess() == curT.Edit:
            # llamar para el copy
            if curT.valueBuffer(u"idproyecto") != curT.valueBufferCopy(u"idproyecto"):
                if not _i.totalizaCostesProyecto(curT.valueBufferCopy(u"idproyecto")):
                    return False
            if not _i.totalizaCostesProyecto(curT.valueBuffer(u"idproyecto")):
                return False

        return True

    def gesttare_comprobarNotificacionesProyecto(self, curProyecto):
        _i = self.iface
        if curProyecto.valueBuffer(u"archivado") != curProyecto.valueBufferCopy(u"archivado"):
            if curProyecto.valueBuffer(u"archivado"):
                _i.compruebaNotificacion("archivado", curProyecto)
            else:
                _i.compruebaNotificacion("desarchivado", curProyecto)
        elif curProyecto.valueBuffer(u"idresponsable") != curProyecto.valueBufferCopy(u"idresponsable"):
            print("notificvamos cambio  responsable??")
            _i.compruebaNotificacion("responsablepro", curProyecto)
        return True

    def gesttare_compruebaNotificacionParticTarea(self, curPart):
        _i = self.iface
        if curPart.modeAccess() == curPart.Insert:
            return _i.compruebaNotificacion("partictarea", curPart)
        elif curPart.modeAccess() == curPart.Del:
            return _i.compruebaNotificacion("delpartictarea", curPart)
        return True

    def gesttare_totalizaCostesProyecto(self, idproyecto=None):
        # _i = self.iface
        curP = qsatype.FLSqlCursor(u"gt_proyectos")
        curP.select(ustr(u"idproyecto = '", idproyecto, u"'"))
        if not curP.first():
            return False
        curP.setModeAccess(curP.Edit)
        curP.refreshBuffer()
        curP.setValueBuffer(u"hdedicadas", proyectos.getIface().commonCalculateField(u"hdedicadas", curP))
        curP.setValueBuffer(u"costeinterno", proyectos.getIface().commonCalculateField(u"costeinterno", curP))
        curP.setValueBuffer(u"costetotal", proyectos.getIface().commonCalculateField(u"costetotal", curP))
        curP.setValueBuffer(u"rentabilidad", proyectos.getIface().commonCalculateField(u"rentabilidad", curP))
        if not curP.commitBuffer():
            return False
        return True

    def gesttare_beforeCommit_gt_partictarea(self, curPart=None):
        _i = self.iface
        # if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_partictarea(curPart):
        #     return False
        
        _i.compruebaNotificacionParticTarea(curPart)

        return True

    def gesttare_beforeCommit_gt_particproyecto(self, curPart=None):
        _i = self.iface
        # if not qsatype.FactoriaModulos.get('flgesttare').iface.afterCommit_gt_particproyecto(curPart):
        #     return False

        if curPart.modeAccess() == curPart.Del:
            if not _i.desasignarTareasProyecto(curPart):
                return False

            if not _i.eliminarNotificacionesProyecto(curPart):
                return False

            _i.compruebaNotificacion("delparticproyecto", curPart)

            # count = qsatype.FLUtil.sqlSelect(u"gt_particproyecto", u"count(*)", ustr(u"idproyecto = '", str(curPart.valueBuffer(u"idproyecto")), u"'"))
            # if count == 0:
            #     return False

        if curPart.modeAccess() == curPart.Insert:
            # nombreProyecto = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"nombre", ustr(u"idproyecto = '", str(curPart.valueBuffer(u"idproyecto")), "'")) or ""
            _i.compruebaNotificacion("particproyecto", curPart)
            # if not _i.crearActualizaciones(u"Añadido participante en proyecto " + nombreProyecto.replace("'", ""), curPart):
            #     return False
        return True

    def gesttare_eliminarNotificacionesProyecto(self, curPart):
        qsatype.FLSqlQuery().execSql("DELETE FROM gt_actualizusuario where idusuario = " + str(curPart.valueBuffer("idusuario")) + " AND idactualizacion IN (SELECT idactualizacion from gt_actualizaciones where tipobjeto = 'proyecto' AND idobjeto = '" + str(curPart.valueBuffer("idproyecto")) + "')")
        qsatype.FLSqlQuery().execSql("DELETE FROM gt_actualizusuario where idusuario = " + str(curPart.valueBuffer("idusuario")) + " AND idactualizacion IN (SELECT idactualizacion from gt_actualizaciones where idtarea in (SELECT idtarea from gt_tareas where idproyecto = '" + str(curPart.valueBuffer("idproyecto")) + "'))")
        # qsatype.FLSqlQuery().execSql("DELETE FROM gt_partictarea where idusuario = " + str(curPart.valueBuffer("idusuario")) + " AND idtarea IN (SELECT idtarea from gt_tareas where idproyecto = '" + curPart.valueBuffer("idproyecto") + "')")
        return True

    def gesttare_desasignarTareasProyecto(self, curPart):
        qsatype.FLSqlQuery().execSql("DELETE FROM gt_partictarea where idusuario = " + str(curPart.valueBuffer("idusuario")) + " AND idtarea IN (SELECT idtarea from gt_tareas where idproyecto = '" + str(curPart.valueBuffer("idproyecto")) + "')")
        return True

    def gesttare_compruebaNotificacion(self, tipo, cursor):
        _i = self.iface
        # tipo_objeto -> gt_tarea, gt_proyecto, gt_comentario, gt_anotacion
        if tipo in ["deltarea", "responsable", "resuelta", "abierta", "cambioFechaEjecucion", "comentario"]:
            tipo_objeto = "gt_tarea"
            idobjeto = cursor.valueBuffer("idtarea")
        elif tipo in ["particproyecto", "archivado", "desarchivado", "responsablepro", "delparticproyecto"]:
            tipo_objeto = "gt_proyecto"
            idobjeto = str(cursor.valueBuffer("idproyecto"))
        # elif tipo in ["comentario"]:
        #     tipo_objeto = "gt_comentario"
        #     idobjeto = cursor.valueBuffer("idcomentario")
        elif tipo in ["partictarea", "delpartictarea"]:
            tipo_objeto = "gt_tarea"
            idobjeto = cursor.valueBuffer("idtarea")
        elif tipo in ["anotacion"]:
            tipo_objeto = "gt_anotacion"
            idobjeto = cursor.valueBuffer("idanotacion")
        else:
            return True
        # Creamos actualizacion y despues notificamos si es necesario
        return _i.creaNotificacion(tipo_objeto, idobjeto, tipo, cursor)
        # deltarea
        # responsable -> Añadido como responsable de una tarea
        # resuelta
        # comentario
        # cambioFechaEjecucion
        # partictarea
        # particproyecto
        return True

    def gesttare_creaNotificacion(self, tipo_objeto, idobjeto, tipo, cursor):
        _i = self.iface
        if tipo in ["deltarea", "responsable", "resuelta", "abierta", "cambioFechaEjecucion"]:
            mensaje = "Tarea: " + cursor.valueBuffer("nombre")
        elif tipo in ["particproyecto", "delparticproyecto", "archivado", "desarchivado", "delproyecto", "responsablepro"]:
            mensaje = "Proyecto: " + qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"nombre", "idproyecto = '{}'".format(str(cursor.valueBuffer(u"idproyecto"))))
        elif tipo in ["comentario", "partictarea", "delpartictarea"]:
            mensaje = "Tarea: " + qsatype.FLUtil.sqlSelect(u"gt_tareas", u"nombre", "idtarea = '{}'".format(cursor.valueBuffer(u"idtarea")))
        elif tipo in ["anotacion"]:
            mensaje = cursor.valueBuffer("nombre")
        else:
            return False

        idUsuario = qsatype.FLUtil.nameUser()
        curActualiz = qsatype.FLSqlCursor(u"gt_actualizaciones")
        curActualiz.setModeAccess(curActualiz.Insert)
        curActualiz.refreshBuffer()
        curActualiz.setValueBuffer(u"tipo", tipo)
        curActualiz.setValueBuffer(u"tipobjeto", tipo_objeto)
        curActualiz.setValueBuffer(u"idobjeto", idobjeto)
        curActualiz.setValueBuffer(u"otros", mensaje)
        curActualiz.setValueBuffer(u"fecha", datetime.date.today())
        curActualiz.setValueBuffer(u"hora", time.strftime('%H:%M:%S'))
        if idUsuario:
            curActualiz.setValueBuffer(u"idusuarioorigen", idUsuario)
        if not curActualiz.commitBuffer():
            return False
        return _i.notificarUsuarios(curActualiz.valueBuffer("idactualizacion"), tipo_objeto, idobjeto, tipo, cursor)

    def gesttare_notificarUsuarios(self, idActualizacion, tipo_objeto, idobjeto, tipo, cursor):
        _i = self.iface
        idUsuario = qsatype.FLUtil.nameUser()
        if tipo in ["deltarea", "resuelta", "abierta","cambioFechaEjecucion", "comentario"]:
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
            while qryParticipantes.next():
                if _i.creaNotificacionUsuario(idActualizacion, qryParticipantes.value(1), tipo_objeto, idobjeto, tipo, cursor):
                    continue
                else:
                    print("error al generar notificacion del usuario")
                    return False
        if tipo in ["archivado", "desarchivado", "delproyecto"]:
            qryParticipantes = qsatype.FLSqlQuery()
            qryParticipantes.setTablesList(u"gt_particproyecto")
            qryParticipantes.setSelect(u"idparticipante,idusuario")
            qryParticipantes.setFrom(ustr(u"gt_particproyecto"))
            qryParticipantes.setWhere("idproyecto = '{}' AND idusuario <> {}".format(str(cursor.valueBuffer(u"idproyecto")), idUsuario))

            try:
                qryParticipantes.setForwardOnly(True)
            except Exception:
                qsatype.Object()

            if not qryParticipantes.exec_():
                return False

            if qryParticipantes.size() == 0:
                return True
            while qryParticipantes.next():
                if _i.creaNotificacionUsuario(idActualizacion, qryParticipantes.value(1), tipo_objeto, idobjeto, tipo, cursor):
                    continue
                else:
                    print("error al generar notificacion del usuario")
                    return False
        elif tipo in ["responsable", "responsablepro", "partictarea", "delpartictarea", "delparticproyecto", "particproyecto"]:
            if tipo == "responsable" and not cursor.valueBuffer("idusuario"):
                return True
            if str(idUsuario) != str(cursor.valueBuffer("idusuario")) and cursor.valueBuffer("idusuario"):
                if _i.creaNotificacionUsuario(idActualizacion, cursor.valueBuffer("idusuario"), tipo_objeto, idobjeto, tipo, cursor):
                    return True
            if tipo == "responsablepro":
                if str(idUsuario) != str(cursor.valueBuffer("idresponsable")) and cursor.valueBuffer("idresponsable"):
                    if _i.creaNotificacionUsuario(idActualizacion, cursor.valueBuffer("idresponsable"), tipo_objeto, idobjeto, tipo, cursor):
                        return True
        return True

    def gesttare_creaNotificacionUsuario(self, idActualizacion, usuarioNotificado, tipo_objeto, idobjeto, tipo, cursor):
        # Si ya tenemos notificacion no hacemos nada
        notificamos = True
        idUsuario = qsatype.FLUtil.nameUser()
        where = u"a.tipobjeto = '" + str(tipo_objeto) + "' AND a.idobjeto = '" + str(idobjeto) + "' AND u.idusuario = '" + str(usuarioNotificado) + "'"
        # if tipo_objeto == "gt_comentario":
        #     where = u"(a.tipobjeto = 'gt_tarea' AND a.idobjeto = '" + str(cursor.valueBuffer("idtarea")) + "') OR (a.tipobjeto = '" + str(tipo_objeto) + "' AND u.idusuario = '" + str(usuarioNotificado) + "' AND a.idobjeto IN (Select idcomentario::VARCHAR from gt_comentarios where idtarea = '" + str(cursor.valueBuffer("idtarea")) + "'))"
        if qsatype.FLUtil.sqlSelect(u"gt_actualizusuario", u"idactualizusuario", ustr(u"idusuario = ", usuarioNotificado, u" AND idactualizacion = ", idActualizacion)):
            return True
        # actualiz = qsatype.FLUtil.quickSqlSelect("gt_actualizusuario u INNER JOIN gt_actualizaciones  ON u.idactualizacion = a.idactualizacion", "a.tipo", "a.tipobjeto = '" + str(tipo_objeto) + "' AND a.idobjeto = '" + str(idobjeto) + "' AND u.idusuario = '" + str(usuarioNotificado) + "'")
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_actualizusuario, gt_actualizaciones")
        q.setSelect(u"a.tipo, a.idactualizacion, u.idactualizusuario")
        q.setFrom(u"gt_actualizusuario u INNER JOIN gt_actualizaciones a ON u.idactualizacion = a.idactualizacion")
        q.setWhere(where)

        if not q.exec_():
            print("Error inesperado")
            return False

        # if q.size() > 1:
        #     print("tengo mas de una actualizacion para este usuario en la tabla??")

        if q.next():
            notificamos = False
            if tipo == "deltarea":
                notificamos = True
            elif tipo in ["delparticproyecto", "delpartictarea"]:
                notificamos = True
                if q.value(0) in ["deltarea"]:
                    notificamos = False
            elif tipo == "resuelta" or tipo == "abierta":
                notificamos = True
            elif tipo == q.value(0):
                notificamos = True
            elif tipo in ["archivado", "desarchivado", "delproyecto"]:
                notificamos = True
            elif tipo in ["responsablepro"]:
                notificamos = True
                if q.value(0) in ["archivado", "desarchivado", "delproyecto"]:
                    notificamos = False
            elif tipo == "comentario":
                notificamos = True
                if q.value(0) in ["deltarea", "resuelta", "abierta", "delpartictarea", "delparticproyecto"]:
                    notificamos = False
            elif tipo == "responsable":
                notificamos = True
                if q.value(0) in ["deltarea", "comentario"]:
                    notificamos = False
            else:
                notificamos = False

            if notificamos:
                qsatype.FLSqlQuery().execSql("DELETE FROM gt_actualizusuario where idactualizusuario = '" + str(q.value(2)) + "'")


        if notificamos:
            if not qsatype.FLUtil.sqlInsert(u"gt_actualizusuario", qsatype.Array([u"idactualizacion", u"idusuario", u"revisada"]), qsatype.Array([idActualizacion, usuarioNotificado, False])):
                return False
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
            idActualizacion = qsatype.FLUtil.sqlSelect(u"gt_actualizaciones", u"idactualizacion", "idobjeto = '{}' AND tipo = '{}'".format(str(cursor.valueBuffer(u"idproyecto")), tipo))
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
                if not qsatype.FLUtil.sqlInsert(u"gt_actualizaciones", qsatype.Array([u"tipo", u"tipobjeto", u"idobjeto", u"fecha", u"hora", "idusuarioorigen"]), qsatype.Array([tipo, u"proyecto", str(cursor.valueBuffer(u"idproyecto")), datetime.date.today(), time.strftime('%H:%M:%S'), idUsuario])):
                    return False
                idActualizacion = qsatype.FLUtil.sqlSelect(u"gt_actualizaciones", u"idactualizacion", "idobjeto = '{}' AND tipo = '{}'".format(str(cursor.valueBuffer(u"idproyecto")), tipo))
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
        if ((cursor.table() == u"gt_tareas") or (cursor.table() == u"gt_partictarea")) and not idActualizacion:
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

        return True

    def gesttare_comprobarUsuarioResponsableProyecto(self, curProyecto):
        if curProyecto.modeAccess() == curProyecto.Insert:
            idUsuario = str(qsatype.FLUtil.nameUser())
            if idUsuario != str(curProyecto.valueBuffer("idresponsable")):
                if not qsatype.FLUtil.sqlInsert(u"gt_particproyecto", qsatype.Array([u"idusuario", u"idproyecto"]), qsatype.Array([curProyecto.valueBuffer("idresponsable"), curProyecto.valueBuffer(u"idproyecto")])):
                    return False
        return True
        # if curProyecto.modeAccess() == curProyecto.Insert:
        #     idUsuario = str(qsatype.FLUtil.nameUser())
        #     if not qsatype.FLUtil.sqlInsert(u"gt_particproyecto", qsatype.Array([u"idusuario", u"idproyecto"]), qsatype.Array([idUsuario, str(curProyecto.valueBuffer(u"idproyecto"))])):
        #         return False
        #     if idUsuario != str(curProyecto.valueBuffer("idresponsable")):
        #         if not qsatype.FLUtil.sqlInsert(u"gt_particproyecto", qsatype.Array([u"idusuario", u"idproyecto"]), qsatype.Array([curProyecto.valueBuffer("idresponsable"), curProyecto.valueBuffer(u"idproyecto")])):
        #             return False
        # elif curProyecto.modeAccess() == curProyecto.Edit:
        #     if curProyecto.valueBuffer("idresponsable") and (curProyecto.valueBuffer("idresponsable") != curProyecto.valueBufferCopy("idresponsable")):
        #         if qsatype.FLUtil.sqlSelect(u"gt_particproyecto", u"idparticipante", ustr(u"idusuario = '", str(curProyecto.valueBuffer("idresponsable")), u"' AND idproyecto = '", str(curProyecto.valueBuffer("idproyecto")), "'")):
        #             return True
        #         if not qsatype.FLUtil.sqlInsert(u"gt_particproyecto", qsatype.Array([u"idusuario", u"idproyecto"]), qsatype.Array([curProyecto.valueBuffer("idresponsable"), str(curProyecto.valueBuffer(u"idproyecto"))])):
        #             return False

        # return True

    def gesttare_comprobarClienteProyecto(self, curProyecto):
        if curProyecto.modeAccess() == curProyecto.Edit:
            if curProyecto.valueBufferCopy(u"idcliente") != curProyecto.valueBuffer(u"idcliente"):
                qsatype.FLSqlQuery().execSql("UPDATE gt_tareas SET idcliente = " + str(curProyecto.valueBuffer("idcliente")) + " where idproyecto = '" + str(curProyecto.valueBuffer("idproyecto")) + "' ")
        return True

    def gesttare_comprobarClienteTarea(self, curTarea):
        if curTarea.modeAccess() == curTarea.Insert:
            id_cliente = qsatype.FLUtil.sqlSelect("gt_proyectos", u"idcliente", "idproyecto = " + str(curTarea.valueBuffer("idproyecto")))
            if id_cliente:
                qsatype.FLSqlQuery().execSql("UPDATE gt_tareas SET idcliente = " + str(id_cliente) + " where idproyecto = '" + str(curTarea.valueBuffer("idproyecto")) + "' ")

        if curTarea.modeAccess() == curTarea.Edit:
            if curTarea.valueBufferCopy(u"idproyecto") != curTarea.valueBuffer(u"idproyecto"): 
                id_cliente = qsatype.FLUtil.sqlSelect("gt_proyectos", u"idcliente", "idproyecto = " + str(curTarea.valueBuffer("idproyecto")))
                if id_cliente:
                    qsatype.FLSqlQuery().execSql("UPDATE gt_tareas SET idcliente = " + str(id_cliente) + " where idproyecto = '" + str(curTarea.valueBuffer("idproyecto")) + "' ")
                else:
                    qsatype.FLSqlQuery().execSql("UPDATE gt_tareas SET idcliente = null where idproyecto = '" + str(curTarea.valueBuffer("idproyecto")) + "' ")

        return True

    def gesttare_comprobarUsuarioResponsable(self, curTarea=None):
        if curTarea.valueBuffer(u"idusuario"):
            if curTarea.valueBufferCopy(u"idusuario") != curTarea.valueBuffer(u"idusuario") or (curTarea.modeAccess() == curTarea.Insert and curTarea.valueBuffer(u"idusuario")):
                if not qsatype.FLUtil.sqlSelect(u"gt_partictarea", u"idparticipante", ustr(u"idusuario = ", curTarea.valueBuffer(u"idusuario"), u" AND idtarea = ", curTarea.valueBuffer(u"idtarea"))):
                    if not qsatype.FLUtil.sqlInsert(u"gt_partictarea", qsatype.Array([u"idusuario", u"idtarea"]), qsatype.Array([curTarea.valueBuffer(u"idusuario"), curTarea.valueBuffer(u"idtarea")])):
                        return False
        return True

    def gesttare_comprobarUsuarioParticProyecto(self, curTarea=None):
        if curTarea.valueBuffer("idusuario"):
            participa = qsatype.FLUtil.sqlSelect("gt_particproyecto", "idparticipante", "idusuario = " + str(curTarea.valueBuffer("idusuario")) + " AND idproyecto = " + str(curTarea.valueBuffer("idproyecto")))
            if participa == None:
                return False
        return True

    def gesttare_comprobarUsuarioParticProyectoTarea(self, idusuario, idproyecto):
        participa = qsatype.FLUtil.sqlSelect("gt_particproyecto", "idparticipante", "idusuario = " + str(idusuario) + " AND idproyecto = " + str(idproyecto))
        if participa == None:
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
                # tipo = u"Cambio de responsable"
                # _i.crearActualizaciones(tipo, curTarea)
                _i.compruebaNotificacion("responsable", curTarea)
            elif curTarea.valueBuffer(u"resuelta") != curTarea.valueBufferCopy(u"resuelta"):
                if curTarea.valueBuffer("resuelta"):
                    _i.compruebaNotificacion("resuelta", curTarea)
                else:
                    _i.compruebaNotificacion("abierta", curTarea)
            elif curTarea.valueBuffer(u"fechavencimiento") != curTarea.valueBufferCopy(u"fechavencimiento"):
                _i.compruebaNotificacion("cambioFechaEjecucion", curTarea)
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
        curT.setValueBuffer(u"hdedicadas", tareas.getIface().commonCalculateField(u"hdedicadas", curT))
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
        hdedicadas = _i.time_to_seconds(str(time))
        return hdedicadas / 3600

    def gesttare_time_to_seconds(self, time):
        seconds = 0
        a_time = str(time).split(":")

        if len(a_time) > 0:
            seconds = seconds + int(a_time[0]) * 3600
        if len(a_time) > 1:
            seconds = seconds + int(a_time[1]) * 60
        if len(a_time) > 2:
            seconds = seconds + int(a_time[2])

        return seconds

    def gesttare_beforeCommit_gt_controlhorario(self, cursor=None):
        # _i = self.iface
        if cursor.modeAccess() == cursor.Del:
            return True
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
        totaltiempo = self.iface.calcula_totaltiempo_horario(cursor)
        if totaltiempo:
            cursor.setValueBuffer("totaltiempo", totaltiempo)
            cursor.setValueBuffer("totaltiempostring", self.iface.seconds_to_time(int(totaltiempo), all_in_hours=True))
        return True

    def gesttare_beforeCommit_gt_controldiario(self, cursor=None):
        # _i = self.iface

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
        if totaltiempo:
            cur_diario.setValueBuffer("totaltiempo", totaltiempo)
            cur_diario.setValueBuffer("totaltiempostring", self.iface.seconds_to_time(int(totaltiempo), all_in_hours=True))
        horasordinarias = self.iface.calcula_horasordinarias_diario(cur_diario)
        if horasordinarias:
            cur_diario.setValueBuffer("horasordinarias", horasordinarias)
            cur_diario.setValueBuffer("horasordinariasstring", self.iface.seconds_to_time(horasordinarias, all_in_hours=True))

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

        totaltiempo = self.iface.calcula_totaltiempo_mensual(idc_mensual)
        cur_mensual.setValueBuffer("totaltiempo", totaltiempo)
        cur_mensual.setValueBuffer("totaltiempostring", self.iface.seconds_to_time(int(totaltiempo), all_in_hours=True))
        cur_mensual.setValueBuffer("horasextra", str(self.iface.calcula_horasextra_mensual(idc_mensual)))
        # cur_mensual.setValueBuffer("horasordinarias", str(self.iface.calcula_horasordinarias_diario(cur_mensual)))
        horasordinarias = self.iface.calcula_horasordinarias_diario(cur_mensual)
        cur_mensual.setValueBuffer("horasordinarias", horasordinarias)
        cur_mensual.setValueBuffer("horasordinariasstring", self.iface.seconds_to_time(horasordinarias, all_in_hours=True))
        if not cur_mensual.commitBuffer():
            print("Ocurrió un error al actualizar el registro mensual")
            return False

        return True

    def gesttare_calcula_totaltiempo_horario(self, cursor):
        if not cursor.valueBuffer("horainicio") or not cursor.valueBuffer("horafin"):
            return None
        try:
            now = str(qsatype.Date())
            # fecha = now[:10]
            fechaAnterior = qsatype.FLUtil().quickSqlSelect("gt_controldiario", "fecha", "idc_diario = '{}'".format(cursor.valueBuffer("idc_diario")))
            horainicio = self.iface.time_to_seconds(cursor.valueBuffer("horainicio"))
            horafin = self.iface.time_to_seconds(cursor.valueBuffer("horafin"))
            fechafin = cursor.valueBuffer("fechafin")
            if qsatype.Date(str(fechaAnterior)) < qsatype.Date(str(fechafin)):
                diferencia = (qsatype.Date(fechafin) - qsatype.Date(str(fechaAnterior)))
                dias = 24 * diferencia.days
                totaltiempo = (self.iface.time_to_seconds(str(dias) + ":00:00") - horainicio) + horafin
            else:
                totaltiempo  = horafin - horainicio
            # totaltiempo = horafin - horainicio
            return totaltiempo
        except Exception as e:
            print(e)
        # formato = "%H:%M:%S"
        # horainicio = str(cursor.valueBuffer("horainicio"))
        # if len(horainicio) == 5:
        #     horainicio += ":00"
        # horafin = str(cursor.valueBuffer("horafin"))
        # if len(horafin) == 5:
        #     horafin += ":00"

        # horafin = horafin.split(":")
        # horainicio = horainicio.split(":")

        # hfin = datetime.timedelta(hours=int(horafin[0]), minutes=int(horafin[1]), seconds=int(horafin[2]))
        # hinicio = datetime.timedelta(hours=int(horainicio[0]), minutes=int(horainicio[1]), seconds=int(horainicio[2]))
        # # hfin = datetime.datetime.strptime(horafin, formato)
        # # hinicio = datetime.datetime.strptime(horainicio, formato)
        # totaltiempo = hfin - hinicio

        # totaltiempo = str(totaltiempo)
        # if len(totaltiempo) < 8:
        #     totaltiempo = "0" + totaltiempo
        # if len(totaltiempo) > 8:
        #     totaltiempo = totaltiempo[8:]
            # print(self.iface.seconds_to_time(auxT, all_in_hours=True))
        return 0

    def gesttare_calcula_totaltiempo_diario(self, idc_diario):
        totaltiempo = qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "SUM(totaltiempo)", "idc_diario = {}".format(idc_diario)) or 0
        # if not totaltiempo or totaltiempo == "None":
        #     return "00:00:00"
        # if len(totaltiempo) < 8:
        #     totaltiempo = "0" + totaltiempo
        # if len(totaltiempo) > 8:
        #     totaltiempo = totaltiempo[8:]
        return totaltiempo

    def gesttare_calcula_horasordinarias_diario(self, cur_diario):
        if not cur_diario.valueBuffer("totaltiempo") or cur_diario.valueBuffer("totaltiempo") == "None":
            return None

        if not cur_diario.valueBuffer("horasextra") or cur_diario.valueBuffer("horasextra") == "None" or str(cur_diario.valueBuffer("horasextra")) == "00:00:00":
            return cur_diario.valueBuffer("totaltiempo")

        # formato = "%H:%M:%S"
        # # totaltiempo = str(cur_diario.valueBuffer("totaltiempo"))
        # # if len(totaltiempo) == 5:
        # #     totaltiempo += ":00"
        # horasextra = str(cur_diario.valueBuffer("horasextra"))
        # if len(horasextra) == 5:
        #     horasextra += ":00"

        # horasextra = datetime.datetime.strptime(horasextra, formato)
        # totaltiempo = datetime.datetime.strptime(totaltiempo, formato)
        # horasordinarias = totaltiempo - horasextra
        # horasordinarias = str(horasordinarias)
        # if len(horasordinarias) < 8:
        #     horasordinarias = "0" + horasordinarias
        # if len(horasordinarias) > 8:
        #     horasordinarias = horasordinarias[8:]
        try:
            totaltiempo = cur_diario.valueBuffer("totaltiempo")
            horasextra = self.iface.time_to_seconds(cur_diario.valueBuffer("horasextra"))
            horasordinarias = totaltiempo - horasextra
            return horasordinarias
            # print(self.iface.seconds_to_time(auxT, all_in_hours=True))
        except Exception as e:
            print(e)
        return 0

    def gesttare_calcula_horaentrada(self, idc_diario):
        return qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "MIN(horainicio)", "idc_diario = {}".format(idc_diario)) or "00:00:00"

    def gesttare_calcula_horasalida(self, idc_diario):
        return qsatype.FLUtil().quickSqlSelect("gt_controlhorario", "MAX(horafin)", "idc_diario = {}".format(idc_diario)) or "00:00:00"

    def gesttare_calcula_totaltiempo_mensual(self, idc_mensual):
        tiempototal = qsatype.FLUtil().quickSqlSelect("gt_controldiario", "SUM(totaltiempo)", "idc_mensual = {}".format(idc_mensual)) or 0
        return tiempototal
        # return self.iface.seconds_to_time(tiempototal.total_seconds(), all_in_hours=True)

    def gesttare_calcula_horasextra_mensual(self, idc_mensual): 
        tiempototal = qsatype.FLUtil().quickSqlSelect("gt_controldiario", "SUM(horasextra)", "idc_mensual = {}".format(idc_mensual)) or "00:00:00"
        if str(tiempototal) == "00:00:00":
            return tiempototal
        return self.iface.seconds_to_time(tiempototal.total_seconds(), all_in_hours=True)


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

    def gesttare_formatearTotalPresupuesto(self, totalPresupuesto):
        if totalPresupuesto < 100:
            totalPresupuesto = str("{:,.2f}".format(totalPresupuesto).replace(",", "@").replace(".", ",").replace("@", "."))
        elif totalPresupuesto >= 100 and totalPresupuesto < 1000:
            totalPresupuesto = str("{:,.0f}".format(totalPresupuesto).replace(",", "@").replace(".", ",").replace("@", "."))
        elif totalPresupuesto >= 1000 and totalPresupuesto < 10000:
            totalPresupuesto = str("{:,.0f}".format(totalPresupuesto).replace(",", "@").replace(".", ",").replace("@", "."))
        elif totalPresupuesto >= 10000 and totalPresupuesto < 100000:
            totalPresupuesto = str("{:,.2f}".format(totalPresupuesto/1000).replace(",", "@").replace(".", ",").replace("@", "."))
            # totalPresupuesto = (locale.format('%.2f', totalPresupuesto/1000, grouping=True, monetary=True))
            totalPresupuesto = str(totalPresupuesto) + "K"
        elif totalPresupuesto >= 100000 and totalPresupuesto < 1000000:
            totalPresupuesto = str("{:,.0f}".format(totalPresupuesto/1000).replace(",", "@").replace(".", ",").replace("@", "."))
            totalPresupuesto = str(totalPresupuesto) + "K"
        # elif totalPresupuesto > 1000000 and totalPresupuesto < 10000000:
        #     totalPresupuesto = (locale.format('%.2f', totalPresupuesto/1000000, grouping=True, monetary=True))
        #     totalPresupuesto = str(totalPresupuesto) + " M"
        else:
            totalPresupuesto = str("{:,.2f}".format(totalPresupuesto/1000000).replace(",", "@").replace(".", ",").replace("@", "."))
            totalPresupuesto = str(totalPresupuesto) + "M"
        totalPresupuesto = str(totalPresupuesto) +" €"
        return totalPresupuesto

    def gesttare_formatearTotalTiempo(self, tiempo):
        if tiempo == None or tiempo =="":
            tiempo = "00:00"
        else:
            # tiempo = self.iface.seconds_to_time(tiempo.total_seconds(), all_in_hours=True)
            tiempo = str(tiempo)
            if len(tiempo) == 8:
                tiempo = tiempo[0:5]
            elif len(tiempo) == 9:
                tiempo = tiempo[0:6]
            else:
                tiempo = tiempo[0:4]
        return tiempo

    def gesttare_completarTareasHito(self, curHito):
        curTarea = qsatype.FLSqlCursor(u"gt_tareas")
        curTarea.select(ustr(u"idhito = '", curHito.valueBuffer("idhito"), u"' AND resuelta = false"))
        while curTarea.next():
            curTarea.setModeAccess(curTarea.Edit)
            curTarea.refreshBuffer()
            curTarea.setValueBuffer("resuelta", True)
            if not curTarea.commitBuffer():
                return False
        return True

    def gesttare_crearHitoInicial(self, curHito):

        user_name = qsatype.FLUtil.nameUser()
        
        # curHito = qsatype.FLSqlCursor("gt_hitosproyecto")
        if not curHito.valueBuffer("fechaterminado"):
            fecha_terminado = qsatype.FLUtil.sqlSelect("gt_proyectos", "fechaterminado", "idproyecto = {}".format(str(curHito.valueBuffer("idproyecto"))))
            curHito.setModeAccess(curHito.Edit)
            curHito.refreshBuffer()
            curHito.setValueBuffer("fechaterminado", fecha_terminado)
            if not curHito.commitBuffer():
                return False

        # curHito.setValueBuffer("idproyecto", curProyecto.valueBuffer("idproyecto"))
        # curHito.setValueBuffer("nombre", "Coordinación")
        # curHito.setValueBuffer("idusuario", user_name)
        # curHito.setValueBuffer("fechainicio", curProyecto.valueBuffer("fechainicio"))
        

        
       
        return True


    def gesttare_borrarTareasHito(self, curHito):
        curTarea = qsatype.FLSqlCursor(u"gt_tareas")
        curTarea.select(ustr(u"idhito = '", curHito.valueBuffer("idhito"), u"'"))
        while curTarea.next():
            curTarea.setModeAccess(curTarea.Del)
            curTarea.refreshBuffer()
            if not curTarea.commitBuffer():
                return False
        return True

    def gesttare_compruebaPermisosPlan(self, accion):
        # saco usuario
        # saco plan
        try:
            usuario = qsatype.FLUtil.nameUser()
            id_compania = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(usuario))
            id_plan = qsatype.FLUtil.quickSqlSelect("aqn_companies", "idplan", "idcompany = '{}'".format(id_compania)) or None
                
        except Exception as e:
            return True

        # if accion == "invitacion" and id_plan == 1:
        #     response = {}
        #     response["status"] = 1
        #     response["resul"] = True
        #     response["msg"] = "Debes tener un plan PROFESIONAL o superior para usar esta funcionalidad"
        #     return response

        if accion == "startstop" and id_plan == 1:
            response = {}
            response["status"] = 1
            response["resul"] = True
            response["msg"] = "Debes tener un plan S o superior para usar esta funcionalidad"
            return response


        if accion == "cliente" and id_plan == 1:
            response = {}
            response["status"] = 1
            response["resul"] = True
            response["msg"] = "Debes tener un plan S o superior para usar esta funcionalidad"
            return response

        if accion == "start" and id_plan == 1 or accion == "start" and id_plan == 2 or accion == "start" and id_plan == 5:
            response = {}
            response["status"] = 1
            response["resul"] = True
            response["msg"] = "Debes tener un plan S o superior para usar esta funcionalidad"
            return response

        if accion == "informes_horizontal" and id_plan == 1:
            data = [{"name": "Proyecto 2", "value": 10, "color": "rgb(204, 41, 22)"}, {"name": "Proyecto 4", "value": 12, "color": "rgb(157, 236, 172)"}, {"name": "Proyecto 1", "value": 20, "color": "rgb(66, 173, 170)"}, {"name": "Proyecto 5", "value": 28, "color": "rgb(255, 198, 141)"}, {"name": "Proyecto 3", "value": 40, "color": "rgb(80 210 206)"}]
            return {"type": "horizontalBarChart", "data": data, "innerText": True, "size": "75", "text": "Tiempo invertido en proyectos"}

        if accion == "informes_pie" and id_plan == 1:
            data = [{"name": "Proyecto 1", "value": 20, "color": "rgb(204, 41, 22)"}, {"name": "Proyecto 2", "value": 10, "color": "rgb(157, 236, 172)"}, {"name": "Proyecto 3", "value": 40, "color": "rgb(66, 173, 170)"}, {"name": "Proyecto 4", "value": 12, "color": "rgb(255, 198, 141)"}, {"name": "Proyecto 5", "value": 28, "color": "rgb(80 210 206)"}]
            return {"type": "pieDonutChart", "data": data, "size": 80, "innerText": True, "text": "Distribución del tiempo en proyectos"}

        if accion == "informes_info" and id_plan == 1:
            horasStyle = {
            "border": "1px solid #dfdfdf",
            "backgroundColor": "white",
            "color": "grey"
            }

            presupuestoStyle = {
                "backgroundColor": "#bababa",
                "color": "#ffffff"
            }

            rentabilidadStyle = {
                "backgroundImage": "linear-gradient(to right, #e79b21, #ffc68d)",
                "color": "#ffffff"
            }
            data = [{"name": "Horas Invertidas", "value": "50", "style": horasStyle} , {"name": "Tareas Completadas", "value": "6", "style": presupuestoStyle}, {"name": "Tareas En Producción", "value": "20", "style" :rentabilidadStyle}]
            return {"type": "labelInfo", "data": data}

        if accion == "titulo_analisis" and id_plan == 1:
            return {"graficosAnalisis": "Datos ficticios"}

        if accion == "porcentaje_hito" and id_plan == 1:
            valor = qsatype.FLUtil.roundFieldValue(0, u"gt_proyectos", u"rentabilidad")
            return valor

        if accion == "rentabilidad_proyecto" and id_plan == 1:
            return [{"type": "pieDonutChart", "data": [{"name": "Rentabilidad", "value": 100, "color": "#50d2ce"}, {"name": "Resto", "value": 0, "color": "#bababa"}], "innerText": True, "animate": True, "size": 90, "showInfo": False}]            

        return True

    def gesttare_revisar_indicadores(self, usuario, recordatorio=None):
        parametros = {}
        # usuario = qsatype.FLUtil.nameUser() 
        atrasada = qsatype.FLUtil.quickSqlSelect("gt_tareas t INNER JOIN gt_proyectos p ON t.idproyecto = p.idproyecto", "COUNT(t.idtarea)", "t.resuelta = false AND t.fechavencimiento < '{}' AND t.idusuario = '{}' AND p.archivado = false".format(str(qsatype.Date())[:10] ,usuario))
        # revisada = qsatype.FLUtil.quickSqlSelect("gt_actualizusuario", "COUNT(idactualizusuario)", "revisada = false AND idusuario = '{}' ".format(str(usuario)))
        revisada_bandeja_fecha = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones INNER JOIN gt_actualizusuario ON gt_actualizaciones.idactualizacion = gt_actualizusuario.idactualizacion", "COUNT(gt_actualizaciones.fecha)", "gt_actualizusuario.revisada = false AND gt_actualizusuario.idusuario = '{}' AND gt_actualizaciones.fecha < CURRENT_DATE AND gt_actualizaciones.tipo <> 'anotacion' AND gt_actualizaciones.tipo <> 'inbox' AND gt_actualizaciones.fecha BETWEEN '2019-11-16' AND '2500-12-20'".format(str(usuario)))
        
        espera_sin_modificacion = qsatype.FLUtil.quickSqlSelect("gt_tareas INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto", "COUNT(idtarea)", "gt_tareas.codestado = 'En espera' AND gt_tareas.resuelta = false AND gt_tareas.idusuario = '{}' AND gt_proyectos.archivado = false AND gt_tareas.ultimamodificacion < CURRENT_DATE - 7".format(str(usuario)))
        # print("revisada: ",revisada)
        if atrasada > 0:
            parametros.update({'atrasadas' : atrasada} )
            # print("tiene tareas atrasadas")
            # self.revisar_tareas_atrasadas(usuario, oParam)
        if revisada_bandeja_fecha > 0:
            parametros.update({'revisada' : revisada_bandeja_fecha} )
        else:
            revisada_bandeja_hora = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones INNER JOIN gt_actualizusuario ON gt_actualizaciones.idactualizacion = gt_actualizusuario.idactualizacion", "COUNT(gt_actualizaciones.fecha)", "gt_actualizusuario.revisada = false AND gt_actualizusuario.idusuario = '{}' AND gt_actualizaciones.hora < CURRENT_TIME - TIME '03:00' AND gt_actualizaciones.tipo <> 'anotacion' AND gt_actualizaciones.tipo <> 'inbox' AND gt_actualizaciones.fecha BETWEEN '2019-11-16' AND '2500-12-20'".format(str(usuario)))
            if revisada_bandeja_hora > 0:
                parametros.update({'revisada' : revisada_bandeja_hora} )

        if espera_sin_modificacion > 0:
            data = []
            q = qsatype.FLSqlQuery()
            q.setTablesList("gt_tareas")
            q.setSelect("gt_tareas.idtarea")
            q.setFrom("gt_tareas INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto")
            q.setWhere("gt_tareas.codestado = 'En espera' AND gt_tareas.resuelta = false AND gt_tareas.idusuario = '{}' AND gt_proyectos.archivado = false AND gt_tareas.ultimamodificacion < CURRENT_DATE - 7".format(str(usuario)))

            if not q.exec_():
                print("Error inesperado")
                return []
            if q.size() > 200:
                return []

            while q.next():
                data.append(q.value(0))
            parametros.update({'espera_sin' : espera_sin_modificacion})
            parametros.update({'idtarea' : data})


        revisada_bandeja_anotar_hora = qsatype.FLUtil.quickSqlSelect("gt_actualizaciones INNER JOIN gt_actualizusuario ON gt_actualizaciones.idactualizacion = gt_actualizusuario.idactualizacion", "COUNT(gt_actualizaciones.fecha)", "gt_actualizusuario.revisada = false AND gt_actualizusuario.idusuario = '{}' AND gt_actualizaciones.fecha < CURRENT_DATE AND (gt_actualizaciones.tipo = 'anotacion' OR gt_actualizaciones.tipo = 'inbox')".format(str(usuario)))

        if revisada_bandeja_anotar_hora > 0:
            parametros.update({'revisada_anotar' : revisada_bandeja_anotar_hora} )

        tarea_sin_modificacion = qsatype.FLUtil.quickSqlSelect("gt_tareas INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto", "COUNT(gt_tareas.idtarea)", "gt_tareas.fechavencimiento is null AND gt_tareas.fechaentrega is null  AND gt_tareas.resuelta = false AND gt_tareas.idusuario = '{}' AND gt_proyectos.archivado = false AND gt_tareas.ultimamodificacion < CURRENT_DATE - 30".format(str(usuario)))

        if tarea_sin_modificacion > 0:
            dataTarea = []
            q = qsatype.FLSqlQuery()
            q.setTablesList("gt_tareas")
            q.setSelect("gt_tareas.idtarea")
            q.setFrom("gt_tareas INNER JOIN gt_proyectos ON gt_tareas.idproyecto = gt_proyectos.idproyecto")
            q.setWhere("gt_tareas.fechavencimiento is null AND gt_tareas.fechaentrega is null  AND gt_tareas.resuelta = false AND gt_tareas.idusuario = '{}' AND gt_proyectos.archivado = false AND gt_tareas.ultimamodificacion < CURRENT_DATE - 30".format(str(usuario)))

            if not q.exec_():
                print("Error inesperado")
                return []
            if q.size() > 200:
                return []

            while q.next():
                dataTarea.append(q.value(0))
            parametros.update({'tarea_sin' : tarea_sin_modificacion})
            parametros.update({'idtarea_planear' : dataTarea})
        return parametros

    # def gesttare_revisar_tareas_atrasadas(self):
    #     print("gesttare_revisar_tareas_atrasadas tiene tareas atrasadas")

    def gesttare_controlFechaModTarea(self, curTarea):
        now = str(qsatype.Date())
        fecha = now[:10]
        curTarea.setValueBuffer("ultimamodificacion", fecha)
        return True


    def gesttare_actualizarModificacion(self, idTarea):
        now = str(qsatype.Date())
        fecha = now[:10]
        if idTarea:
            # if not qsatype.FLUtil.sqlUpdate("gt_tareas", "fechacreacion", datetime.date.today(), "idtarea = ", str(idtarea)):
            #     print("???????")
            #     return False
            if not qsatype.FLSqlQuery().execSql("UPDATE gt_tareas SET ultimamodificacion = '" + str(fecha) + "' where idtarea = " + str(idTarea)):
                return False
        return True


    def __init__(self, context=None):
        super().__init__(context)

    def afterCommit_gt_comentarios(self, curComentario=None):
        return self.ctx.gesttare_afterCommit_gt_comentarios(curComentario)

    def afterCommit_gt_tareas(self, curTarea=None):
        return self.ctx.gesttare_afterCommit_gt_tareas(curTarea)

    def beforeCommit_gt_tareas(self, curTarea=None):
        return self.ctx.gesttare_beforeCommit_gt_tareas(curTarea)

    def afterCommit_gt_timetracking(self, cursor=None):
        return self.ctx.gesttare_afterCommit_gt_timetracking(cursor)

    def beforeCommit_gt_partictarea(self, curPart=None):
        return self.ctx.gesttare_beforeCommit_gt_partictarea(curPart)

    def beforeCommit_gt_particproyecto(self, curPart=None):
        return self.ctx.gesttare_beforeCommit_gt_particproyecto(curPart)

    def crearActualizaciones(self, tipo, cursor=None):
        return self.ctx.gesttare_crearActualizaciones(tipo, cursor)

    def comprobarUsuarioResponsable(self, curTarea=None):
        return self.ctx.gesttare_comprobarUsuarioResponsable(curTarea)

    def comprobarUsuarioParticProyecto(self, curTarea=None):
        return self.ctx.gesttare_comprobarUsuarioParticProyecto(curTarea)

    def comprobarUsuarioParticProyectoTarea(self, idusuario, idproyecto):
        return self.ctx.gesttare_comprobarUsuarioParticProyectoTarea(idusuario, idproyecto)

    def comprobarActualizacionesTareas(self, curTarea=None):
        return self.ctx.gesttare_comprobarActualizacionesTareas(curTarea)

    def compruebaNotificacion(self, tipo, cursor):
        return self.ctx.gesttare_compruebaNotificacion(tipo, cursor)

    def creaNotificacion(self, tipo_objeto, idobjeto, tipo, cursor):
        return self.ctx.gesttare_creaNotificacion(tipo_objeto, idobjeto, tipo, cursor)

    def notificarUsuarios(self, idActualizacion, tipo_objeto, idobjeto, tipo, cursor):
        return self.ctx.gesttare_notificarUsuarios(idActualizacion, tipo_objeto, idobjeto, tipo, cursor)

    def creaNotificacionUsuario(self, idActualizacion, usuarioNotificado, tipo_objeto, idobjeto, tipo, cursor):
        return self.ctx.gesttare_creaNotificacionUsuario(idActualizacion, usuarioNotificado, tipo_objeto, idobjeto, tipo, cursor)

    def afterCommit_gt_proyectos(self, curProyecto):
        return self.ctx.gesttare_afterCommit_gt_proyectos(curProyecto)

    def beforeCommit_gt_proyectos(self, curProyecto):
        return self.ctx.gesttare_beforeCommit_gt_proyectos(curProyecto)

    def beforeCommit_gt_hitosproyecto(self, curHito):
        return self.ctx.gesttare_beforeCommit_gt_hitosproyecto(curHito)

    def afterCommit_gt_hitosproyecto(self, curHito):
        return self.ctx.gesttare_afterCommit_gt_hitosproyecto(curHito)

    def comprobarUsuarioResponsableProyecto(self, curProyecto):
        return self.ctx.gesttare_comprobarUsuarioResponsableProyecto(curProyecto)

    def comprobarClienteProyecto(self, curProyecto):
        return self.ctx.gesttare_comprobarClienteProyecto(curProyecto)

    def comprobarClienteTarea(self, curTarea):
        return self.ctx.gesttare_comprobarClienteTarea(curTarea)

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

    def compruebaNotificacionParticTarea(self, curPart):
        return self.ctx.gesttare_compruebaNotificacionParticTarea(curPart)

    def comprobarNotificacionesProyecto(self, curProyecto):
        return self.ctx.gesttare_comprobarNotificacionesProyecto(curProyecto)

    def totalizaCostesProyecto(self, idproyecto):
        return self.ctx.gesttare_totalizaCostesProyecto(idproyecto)

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

    def formatearTotalPresupuesto(self, totalPresupuesto):
        return self.ctx.gesttare_formatearTotalPresupuesto(totalPresupuesto)

    def formatearTotalTiempo(self,tiempo):
        return self.ctx.gesttare_formatearTotalTiempo(tiempo)

    def crearHitoInicial(self, curProyecto):
        return self.ctx.gesttare_crearHitoInicial(curProyecto)

    def completarTareasHito(self, curHito):
        return self.ctx.gesttare_completarTareasHito(curHito)

    def borrarTareasHito(self, curHito):
        return self.ctx.gesttare_borrarTareasHito(curHito)

    def compruebaPermisosPlan(self, accion):
        return self.ctx.gesttare_compruebaPermisosPlan(accion)

    def revisar_indicadores(self, usuario, recordatorio=None):
        return self.ctx.gesttare_revisar_indicadores(usuario, recordatorio=None)

    def revisar_tareas_atrasadas(self):
        return self.ctx.gesttare_revisar_tareas_atrasadas()

    def actualizarModificacion(self, idTarea):
        return self.ctx.gesttare_actualizarModificacion(idTarea)

    def controlFechaModTarea(self, curTarea):
        return self.ctx.gesttare_controlFechaModTarea(curTarea)


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
