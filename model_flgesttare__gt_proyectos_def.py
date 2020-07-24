# @class_declaration interna #
import json
import re
import hashlib
from YBLEGACY import qsatype
from YBUTILS import notifications
import datetime
import time

class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
from models.flgesttare import flgesttare_def
from YBUTILS.APIQSA import APIQSA


class gesttare(interna):

    def gesttare_get_model_info(self, model, data, ident, template, where_filter):
        if template == "list":
            return {"groupBoxPadre": "Nº DE PROYECTOS: {}".format(ident["COUNT"])}
        if template == "master":
            return {"groupBoxPadre": "Nº DE PROYECTOS: {}".format(ident["PAG"]["COUNT"])}
        if template == "rentabilidadProyectos":
            return {"groupBoxPadre": "Nº DE PROYECTOS: {}".format(ident["PAG"]["COUNT"])}
        return None

    def get_model_info(self, model, data, ident, template, where_filter):
        return self.ctx.gesttare_get_model_info(model, data, ident, template, where_filter)

    def gesttare_getDesc(self):
        desc = "nombre"
        return desc

    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        if template == "master":
            fields = [
                {'verbose_name': 'nombreCliente', 'func': 'field_nombreCliente'},
                {'verbose_name': 'Color fondo estado', 'func': 'color_fondo_estado'},
                {'verbose_name': 'Responsable', 'func': 'field_usuario'},
                {'verbose_name': 'Color responsable', 'func': 'color_responsable'},
                {'verbose_name': 'Color nombre', 'func': 'color_nombre'}
            ]
        elif template == "proyectosarchivados":
            fields = [
                {'verbose_name': 'nombreCliente', 'func': 'field_queryNombreCliente'}
            ]

        elif template == "rentabilidadProyectos":
            fields = [
                {'verbose_name': 'Color fondo estado query', 'func': 'color_fondo_estado_query'},
                {'verbose_name': 'Color fondo resultado', 'func': 'color_fondo_resultado'},
                {'verbose_name': 'nombreCliente', 'func': 'field_queryNombreCliente'}
            ]
        return fields

    def gesttare_field_nombreCliente(self, model):
        usuario = qsatype.FLUtil.nameUser()
        nombre_cliente = ""
        id_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = {}".format(str(usuario)))
        try:
            if not model.idcliente:
                return nombre_cliente
            if model.idcompany.idcompany == id_company:
                nombre_cliente = model.idcliente.nombre
        except Exception as e:
            print(e)
            pass
        return nombre_cliente

    def gesttare_field_queryNombreCliente(self, model):
        tengocliente = ""
        if model["gt_proyectos.idcliente"]:
            tengocliente = qsatype.FLUtil.sqlSelect("gt_clientes", "nombre", "idcliente = '{}'".format(model["gt_proyectos.idcliente"]))
            if not tengocliente:
                return ""

        return tengocliente

    def gesttare_field_usuario(self, model):
        nombre_usuario = ""
        # if hasattr(model.idresponsable, 'usuario'):
        #     print("el valor es: ",model.idresponsable.usuario)
        try:
            if not model.idresponsable:
                return nombre_usuario
            nombre_usuario = "@" + model.idresponsable.usuario
        except Exception:
            pass
        return nombre_usuario

    def gesttare_color_nombre(self, model):
        username = qsatype.FLUtil.nameUser()
        id_company = qsatype.FLUtil.quickSqlSelect("aqn_user", "idcompany", "idusuario = '{}'".format(username))
        tipo_participante = qsatype.FLUtil.quickSqlSelect("gt_particproyecto", "tipo", "idusuario = '{}' AND idproyecto = {}".format(username, str(model.idproyecto)))
        # if tipo_participante == "observador":
        #     return "OBSER "
        # if model.idcompany.idcompany != id_company:
        #     return "COL "
        # else:
        #     return "INTERNO_EMPRESA "

        return ""

    def gesttare_color_fondo_estado(self, model):
        # try:
        if model.estado:
            if model.estado == "Abierto":
                return "naranja"
            elif model.estado == "Suspendido":
                return "lila"
            elif model.estado == "Terminado":
                return "verde"
            elif model.estado== "Cancelado":
                return "rojo"
            elif model.estado == "Por iniciar":
                return "amarillo"
        # except Exception:
        #     pass
        return ""

    def gesttare_color_fondo_estado_query(self, model):
        # try:
        if model['gt_proyectos.estado']:
            if model['gt_proyectos.estado'] == "Abierto":
                return "naranja"
            elif model['gt_proyectos.estado'] == "Suspendido":
                return "lila"
            elif model['gt_proyectos.estado'] == "Terminado":
                return "verde"
            elif model['gt_proyectos.estado'] == "Cancelado":
                return "rojo"
            elif model['gt_proyectos.estado'] == "Por iniciar":
                return "amarillo"
        # except Exception:
        #     pass
        return ""

    def gesttare_color_fondo_resultado(self, model):
        # try:
        if model['resultado'] or model['resultado'] == 0:
            if model['resultado'] > 0:
                return "verdeResultado"
            elif model['resultado'] < 0:
                return "rojoResultado"
            else:
                return "naranjaResultado"
        # except Exception:
        #     pass
        return ""

    def gesttare_color_responsable(self, model):
        if hasattr(model.idresponsable, 'idusuario'):
            return "responsable"

        return ""

    def gesttare_actNuevoPartic(self, oParam, cursor):
        response = {}
        if "idusuario" not in oParam:
            # idUsuario = cursor.valueBuffer("idusuario")
            qryUsuarios = qsatype.FLSqlQuery()
            qryUsuarios.setTablesList(u"aqn_user")
            qryUsuarios.setSelect(u"idusuario, nombre")
            qryUsuarios.setFrom(ustr(u"aqn_user"))
            # qryUsuarios.setWhere(ustr(u"idusuario <> '", idUsuario, u"'"))
            qryUsuarios.setWhere(ustr(u"1 = 1"))
            if not qryUsuarios.exec_():
                return False

            opts = []
            while qryUsuarios.next():
                tengousuario = qsatype.FLUtil.sqlSelect("gt_particproyecto", "idusuario", "idusuario = '{}' AND idproyecto = '{}'".format(qryUsuarios.value("idusuario"), cursor.valueBuffer("idproyecto")))
                value = False
                if tengousuario:
                    value = True

                opts.append({"key": qryUsuarios.value("idusuario"), "label": qryUsuarios.value("nombre"), "value": value})

            response['status'] = -1
            response['data'] = {}
            response['params'] = [
                {
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "rel": "aqn_user",
                    "style": {
                        "width": "100%"
                    },
                    "tipo": 180,
                    "verbose_name": "Participantes",
                    "label": "Participantes",
                    "function": "getParticCompaniaUsu",
                    "key": "idusuario",
                    "desc": "usuario",
                    "validaciones": None,
                    "required": False,
                    "opts": opts
                }
            ]
            return response
        else:
            participantes = json.loads(oParam["idusuario"])
            if not participantes:
                return True
            for p in participantes:
                curPartic = qsatype.FLSqlCursor("gt_particproyecto")
                curPartic.select("idusuario = '{}' AND idproyecto = '{}'".format(p, cursor.valueBuffer("idproyecto")))
                curPartic.refreshBuffer()

                if curPartic.first():
                    if participantes[p] is False:
                        curPartic.setModeAccess(cursor.Del)
                        curPartic.refreshBuffer()
                        if not curPartic.commitBuffer():
                            return False
                else:
                    if participantes[p] is True:
                        curPartic.setModeAccess(curPartic.Insert)
                        curPartic.refreshBuffer()
                        curPartic.setValueBuffer("idusuario", p)
                        curPartic.setValueBuffer("idproyecto", cursor.valueBuffer("idproyecto"))
                        if not curPartic.commitBuffer():
                            return False
            response["resul"] = True
            response["msg"] = "Actualizados los participantes"
            return response

    def gesttare_getFilters(self, model, name, template=None):
        filters = []
        if name == 'proyectosusuario':
            # proin = "("
            proin = []
            usuario = qsatype.FLUtil.nameUser()
            curProyectos = qsatype.FLSqlCursor("gt_particproyecto")
            curProyectos.select("idusuario = '" + str(usuario) + "'")
            while curProyectos.next():
                curProyectos.setModeAccess(curProyectos.Browse)
                curProyectos.refreshBuffer()
                proin.append(curProyectos.valueBuffer("idproyecto"))
                # proin = proin + "'" + curProyectos.valueBuffer("idproyecto") + "', "
            # proin = proin + " null)"
            # q = qsatype.FLSqlQuery()
            # q.setTablesList(u"gt_proyectos, gt_particproyecto")
            # q.setSelect(u"t.idproyecto")
            # q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.idproyecto=p.idproyecto")
            # q.setWhere(u"p.idusuario = '" + usuario + "' AND  t.idcompania = 1")

            # if not q.exec_():
            #     return []
            # if q.size() > 100:
            #     return []

            # while q.next():
            #     proin.append(q.value("idproyecto"))
            return [{'criterio': 'idproyecto__in', 'valor': proin, 'tipo': 'q'}]
        return filters

    def gesttare_check_permissions(self, model, prefix, pk, template, acl, accion):
        if accion == "delete":
            nombreUsuario = qsatype.FLUtil.nameUser()
            idcompanyUser = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", u"idusuario = '" + nombreUsuario + u"'")
            idcompanyProject = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"idcompany", ustr(u" idproyecto = '", pk, "'"))
            if idcompanyUser != idcompanyProject:
                return False
        if template == "formRecord":
            nombreUsuario = qsatype.FLUtil.nameUser()
            pertenece = qsatype.FLUtil.sqlSelect(u"gt_particproyecto", u"idusuario", ustr(u"idusuario = '", nombreUsuario, u"' AND idproyecto = '", pk, "'"))
            administrador = qsatype.FLUtil.sqlSelect("auth_user", "is_superuser", "username = '{}'".format(str(nombreUsuario)))
            idcompanyUser = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", u"idusuario = '" + nombreUsuario + u"'")
            idcompanyProject = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"idcompany", ustr(u" idproyecto = '", pk, "'"))
            # if not pertenece and not administrador or idcompanyUser != idcompanyProject:
            # if idcompanyUser != idcompanyProject or (not administrador and not pertenece)not pertenece and not administrador or idcompanyUser != idcompanyProject:
            # if not ((administrador and (idcompanyUser != idcompanyProject or participante)) or (not administrador and pertenece))
            if not (pertenece or (administrador and (idcompanyUser == idcompanyProject))):
                return False
        return True

    def gesttare_getProyectosUsuario(self, oParam):
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"gt_proyectos, gt_particproyecto")
        q.setSelect(u"p.idproyecto, t.nombre")
        q.setFrom(u"gt_proyectos t LEFT JOIN gt_particproyecto p ON t.idproyecto=p.idproyecto LEFT JOIN gt_clientes c ON c.idcliente = t.idcliente")
        q.setWhere(u"p.idusuario = '" + qsatype.FLUtil.nameUser() + "' AND (UPPER(t.nombre) like UPPER('%" + oParam["val"] + "%') OR UPPER(c.codcliente) LIKE UPPER('%" + oParam["val"] + "%'))AND NOT archivado GROUP BY p.idproyecto, t.nombre  ORDER BY t.nombre LIMIT 7")
        # q.setWhere(u"p.idusuario = '" + qsatype.FLUtil.nameUser() + "' AND UPPER(t.nombre) like UPPER('%" + oParam["val"] + "%') AND t.idcompania = 1  ORDER BY t.nombre LIMIT 7")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 100:
            print("sale por aqui")
            return []

        while q.next():
            # descripcion = str(q.value(2)) + "€ " + q.value(1)

            des = str(q.value(1))
            codcliente = qsatype.FLUtil.sqlSelect("gt_proyectos INNER JOIN gt_clientes ON gt_clientes.idcliente = gt_proyectos.idcliente", "gt_clientes.codcliente", "gt_proyectos.idproyecto = '" + str(q.value(0)) + "'") or None
            if codcliente:
                des = "#" + codcliente + " " + des
            # if q.value(2):
            #     print(q.value(2))
            #     codcliente = qsatype.FLUtil.sqlSelect(u"gt_clientes", u"codcliente", ustr(u"idcliente = '", str(q.value(2)), u"'"))
            #     if codcliente:
            #         des = "#" + str(codcliente) + " " + des 
            data.append({"idproyecto": q.value(0), "nombre": des, "suggestion": q.value(1)})

        return data

    def gesttare_dameEmailCreaTarea(self, oParam, cursor):
        response = {}
        if "email" not in oParam:
            # "Javier Cantos Cañete" <javier.cantos@makinando.es>
            # val = str(cursor.valueBuffer("idproyecto")) + "@convert.dailyjob.io"
            val = '"' + str(cursor.valueBuffer("nombre")) + '" <' + str(cursor.valueBuffer("idproyecto")) + "@convert.dailyjob.io" + '>'
            response['status'] = -1
            response['data'] = {}
            response['buttons'] = False
            response['title'] = "Copiar en el portapapeles: Ctrl+C"
            response['params'] = [
                {
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "rel": "gt_proyectos",
                    "style": {
                        "width": "100%"
                    },
                    "tipo": 3,
                    "verbose_name": "Email",
                    "label": "Email",
                    "key": "idusuario",
                    "disabled": False,
                    "value": val,
                    "validaciones": None,
                    "required": False,
                    "select": True
                }
            ]
            return response
        else:
            return True

    def gesttare_actInvitarExterno(self, oParam, cursor):
        usuario = qsatype.FLUtil.nameUser()
        return True
        response = {}
        if not re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', oParam["email"].lower()):
            print("Correo incorrecto")
            response["status"] = 1
            response["msg"] = "Formato correo intorrecto"
            return response
        # usuario = qsatype.FLUtil.nameUser()
        curUsuario = qsatype.FLSqlCursor("aqn_user")
        curUsuario.select("email = '" + str(oParam["email"]) + "'")
        if not curUsuario.next():
            # response["status"] = 1
            # response["msg"] = "No existe usuario"
            # return response
            codifica = oParam["email"] + str(cursor.valueBuffer("idproyecto"))
            hashcode = hashlib.md5(codifica.encode('utf-8')).hexdigest()
            curInvitacion = qsatype.FLSqlCursor(u"aqn_invitations")
            curInvitacion.setModeAccess(curInvitacion.Insert)
            curInvitacion.refreshBuffer()
            curInvitacion.setValueBuffer(u"email", oParam["email"])
            curInvitacion.setValueBuffer(u"hashcode", hashlib.md5(hashcode.encode('utf-8')).hexdigest())
            # curInvitacion.setValueBuffer(u"idcompany", idcompany)
            curInvitacion.setValueBuffer(u"idcompany", cursor.valueBuffer("idcompany"))
            curInvitacion.setValueBuffer(u"idproyecto", cursor.valueBuffer("idproyecto"))
            curInvitacion.setValueBuffer(u"fecha", str(qsatype.Date())[:10])
            curInvitacion.setValueBuffer(u"activo", True)
            curInvitacion.setValueBuffer(u"tipo", "colaborador")
            if not curInvitacion.commitBuffer():
                return False

            params = {
                "email": curInvitacion.valueBuffer("email"),
                "tipo_mensaje": "invitacion_proyecto",
                "hashcode": curInvitacion.valueBuffer("hashcode")
            }
            APIQSA.entry_point('post', "aqn_precompanies", usuario, params, "post")    
        else:
            curUsuario.setModeAccess(curUsuario.Browse)
            curUsuario.refreshBuffer()
            idcompany = curUsuario.valueBuffer("idcompany")
            # Comprobamos que no existe usuario con ese email para esa compañia
            if idcompany == cursor.valueBuffer("idcompany"):
                response["status"] = 1
                response["msg"] = "El usuario ya pertenece a la compañia"
                return response
            else:
                print("aqui enviamos la invitacion")
                codifica = oParam["email"] + str(cursor.valueBuffer("idproyecto"))
                hashcode = hashlib.md5(codifica.encode('utf-8')).hexdigest()
                curInvitacion = qsatype.FLSqlCursor(u"aqn_invitations")
                curInvitacion.setModeAccess(curInvitacion.Insert)
                curInvitacion.refreshBuffer()
                curInvitacion.setValueBuffer(u"email", oParam["email"])
                curInvitacion.setValueBuffer(u"hashcode", hashlib.md5(hashcode.encode('utf-8')).hexdigest())
                # curInvitacion.setValueBuffer(u"idcompany", idcompany)
                curInvitacion.setValueBuffer(u"idcompany", cursor.valueBuffer("idcompany"))
                curInvitacion.setValueBuffer(u"idproyecto", cursor.valueBuffer("idproyecto"))
                curInvitacion.setValueBuffer(u"fecha", str(qsatype.Date())[:10])
                curInvitacion.setValueBuffer(u"activo", True)
                curInvitacion.setValueBuffer(u"tipo", "pp")
                if not curInvitacion.commitBuffer():
                    return False
                _i = self.iface
                if not _i.envioMailInvitacion(curInvitacion.valueBuffer("email"), cursor.valueBuffer("nombre"), curInvitacion.valueBuffer("hashcode")):
                    return False
        response = {}
        response["resul"] = True
        response["msg"] = "Invitación enviada correctamente"
        return response

    def gesttare_envioMailInvitacion(self, email, nombreProyecto, hashcode, invi):
        usuario = qsatype.FLUtil.nameUser()
        if usuario != "admin":
            idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
            nombreCompania = qsatype.FLUtil.sqlSelect(u"aqn_companies", u"nombre", ustr(u"idcompany = '", str(idcompany), u"'"))
        else:
            nombreCompania = ""
        username = qsatype.FLUtil.sqlSelect(u"aqn_user", u"usuario", u"email = '" + str(email) + u"'")
        # urlJoin = "https://app.dailyjob.io/cooperate/" + hashcode
        urlJoin = "http://127.0.0.1:8000/cooperate/" + hashcode + "/" + str(invi)
        # cuerpo = "<img src='https://app.dailyjob.io/static/dist/img/logo/logo.png'/>"
        # cuerpo += "<br><a href='" + urlJoin + "''>Unirse DailyJob</a>"
        # cuerpo += "<br>"

        # urlJoin = "https://app.dailyjob.io/cooperate/" + hashcode

        cuerpo = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" style="" class=" js flexbox flexboxlegacy canvas canvastext webgl no-touch geolocation postmessage websqldatabase indexeddb hashchange history draganddrop websockets rgba hsla multiplebgs backgroundsize borderimage borderradius boxshadow textshadow opacity cssanimations csscolumns cssgradients cssreflections csstransforms csstransforms3d csstransitions fontface generatedcontent video audio localstorage sessionstorage webworkers no-applicationcache svg inlinesvg smil svgclippaths js csstransforms csstransforms3d csstransitions responsejs "><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>Invitación Dailyjob</title><!-- Designed by https://github.com/kaytcat --><!-- Header image designed by Freepik.com --><style type="text/css">/* Take care of image borders and formatting */img { max-width: 600px; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;}a img { border: none; }table { border-collapse: collapse !important; }#outlook a { padding:0; }.ReadMsgBody { width: 100%; }.ExternalClass {width:100%;}.backgroundTable {margin:0 auto; padding:0; width:100% !important;}table td {border-collapse: collapse;}.ExternalClass * {line-height: 115%;}/* General styling */td {    font-family: Arial, sans-serif;}body {    -webkit-font-smoothing:antialiased;    -webkit-text-size-adjust:none;    width: 100%;    height: 100%;    color: #6f6f6f;    font-weight: 400;    font-size: 18px;}h1 {    margin: 10px 0;}a {    color: #27aa90;    text-decoration: none;}.force-full-width {    width: 100% !important;}.body-padding {    padding: 0 75px;}</style><style type="text/css" media="screen">        @media screen {            @import url(https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);            /* Thanks Outlook 2013! */            body {                font-family: "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif" !important;            }            .w280 {                width: 280px !important;            }        }</style><style type="text/css" media="only screen and (max-width: 480px)">    /* Mobile styles */    @media only screen and (max-width: 480px) {        table[class*="w320"] {            width: 320px !important;        }        td[class*="w320"] {            width: 280px !important;            padding-left: 20px !important;            padding-right: 20px !important;        }        img[class*="w320"] {            width: 250px !important;            height: 67px !important;        }        td[class*="mobile-spacing"] {            padding-top: 10px !important;            padding-bottom: 10px !important;        }        *[class*="mobile-hide"] {            display: none !important;        }        *[class*="mobile-br"] {            font-size: 12px !important;        }        td[class*="mobile-w20"] {            width: 20px !important;        }        img[class*="mobile-w20"] {            width: 20px !important;        }        td[class*="mobile-center"] {            text-align: center !important;        }        table[class*="w100p"] {            width: 100% !important;        }        td[class*="activate-now"] {            padding-right: 0 !important;            padding-top: 20px !important;        }        [class="mobile-block"] {            width: 100% !important;            display: block !important;        }    }</style>                                  </head><body offset="0" class="body ui-sortable" style="padding: 0px; margin: 0px; display: block; background: rgb(238, 235, 235); text-size-adjust: none; -webkit-font-smoothing: antialiased; width: 100%; height: 100%; color: rgb(111, 111, 111); font-weight: 400; font-size: 18px; cursor: auto; overflow: visible;" bgcolor="#eeebeb"><div data-section-wrapper="=" 1""="" align="center" valign="top" style="font-family: Arial, sans-serif;border-collapse: collapse;">    <center>        <table data-section="1" style="margin: 0px auto; border-collapse: collapse !important; background-color: rgb(255, 255, 255);" cellspacing="0" cellpadding="0" width="600" class="w320" bgcolor="#ffffff">            <tbody><tr>                <td data-slot-container="1" style="text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                    <div data-slot="image" data-param-padding-top="50" data-param-padding-bottom="50" style="padding-top: 50px; padding-bottom: 25px;">                        <a href="http://dailyjob.io" target="_blank" rel="noopener noreferrer"><img class="w320 fr-view" width="311" height="83" src="http://dailyjob.io/img-mailing/color-horizontal.png" alt="company logo" style="max-width: 600px; outline: none; text-decoration: none; border: none; width: 394px; height: 96px;" /><br /></a>                    </div>                </td>            </tr>        </tbody></table>    </center></div><div data-section-wrapper="=" 1""="">    <center>        <table data-section="1" cellspacing="0" cellpadding="0" width="600" class="w320" style="background-color: rgb(255, 255, 255); border-collapse: collapse !important;" bgcolor="#ffffff">            <tbody><tr>                <td style="font-family: Arial, sans-serif;border-collapse: collapse;">                    <table cellspacing="0" cellpadding="0" width="100%" style="border-collapse: collapse !important;">                        <tbody><tr>                            <td data-slot-container="1" style="font-size: 18px;font-weight: 600;color: #ffffff;text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="mobile-spacing ui-sortable">                            <div data-slot="text" data-param-padding-top="" style="padding-top: 0px; padding-bottom: 20px;" data-param-padding-bottom=""><div style="padding: 20px 10%;"><div style="text-align: justify;"><span style="font-size: 14px;"><span style="color: #293333;">¡Hola! <strong><span style="color: #2d95c1;">' + username + '</span></strong></span></span></div><div style="text-align: justify;"><br /></div><div style="text-align: justify;"><span style="font-size: 14px;"><span style="color: #293333;"><strong><span style="color: #2d95c1;">' + nombreCompania + '</span></strong> te ha ha enviado una invitación para unirte al proyecto <strong><span style="color: #2d95c1;">' + nombreProyecto + '</span></strong></span></div><div style="text-align: justify;"><br /></div><div style="text-align: justify;"><span style="font-size: 14px;"><span style="color: #293333;">Para aceptar la invitación, haz clic en el siguiente enlace:</span></span></div></div><div style="padding: 20px 10%;"><span style="font-size: 18px;"><span style="color: #2d95c1;"><a href="' + urlJoin + '">Ir a link' '</a></span></span></div></div></td>                        </tr>                        <tr>                            <td data-slot-container="1" style="font-size: 24px;text-align: center;padding: 0 75px;color: #6f6f6f;font-family: Arial, sans-serif;border-collapse: collapse;" class="w320 mobile-spacing ui-sortable">                            </td>                        </tr>                    </tbody></table>                    <table cellspacing="0" cellpadding="0" width="100%" style="border-collapse: collapse !important;">                        <tbody><tr>                            <td data-slot-container="1" style="font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                            </td>                        </tr>                    </tbody></table>                </td>            </tr>        </tbody></table>    </center></div><div data-section-wrapper="one-column">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0px auto; width: 600px; border-collapse: collapse !important; background-color: rgb(255, 255, 255);" class="w320" cellpadding="0" cellspacing="0" width="600" bgcolor="#ffffff">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="one-column" bgcolor="#ffffff" style="background-color: rgb(255, 255, 255);">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0px auto; width: 600px; border-collapse: collapse !important; background-color: rgb(255, 255, 255);" class="w320" cellpadding="0" cellspacing="0" width="600" bgcolor="#ffffff">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="one-column">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0 auto;border-collapse: collapse !important;width: 600px;" class="w320" cellpadding="0" cellspacing="0" width="600">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="one-column">                                <div data-section-wrapper="1"><center>    <table data-section="1" style="margin: 0 auto;border-collapse: collapse !important;width: 600px;" class="w320" cellpadding="0" cellspacing="0" width="600">        <tbody><tr>            <td data-slot-container="1" valign="top" class="mobile-block ui-sortable" style="padding-left: 5px; padding-right: 5px;">            </td>        </tr>    </tbody></table></center></div>                            </div><div data-section-wrapper="=" 1""="">    <center>        <table data-section="1" cellspacing="0" cellpadding="0" width="600" class="w320" bgcolor="#2d95c1" style="background-color: #293333; border-collapse: collapse !important;">            <tbody><tr>                <td style="font-family: Arial, sans-serif;border-collapse: collapse;">                    <table cellspacing="0" cellpadding="0" class="force-full-width" style="border-collapse: collapse !important;width: 100% !important;">                        <tbody><tr>                            <td data-slot-container="1" style="text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                            <div data-slot="image" data-param-padding-top="20" style="padding-top: 20px; padding-bottom: 30px;" data-param-padding-bottom="30"><a href="http://dailyjob.io" target="_blank" rel="noopener noreferrer"><img src="http://dailyjob.io/img-mailing/blanco-vertical.png" alt="An image" class="fr-view" style="width: 96px; height: 68.6377px;" /><br /></a><div style="clear:both"></div>                            </div>                            </td>                        </tr>                        <tr>                            <td data-slot-container="1" style="color: #f0f0f0;font-size: 14px;text-align: center;padding-bottom: 4px;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                                <div data-slot="text">© 2019 Todos los derechos reservados - <a data-bcup-haslogintext="no" href="mailto:soporte@dailyjob.io" style="color: #ffffff;">Contacto</a><br /><br /></div>                            </td>                        </tr>                        <tr>                            <td data-slot-container="1" style="color: #27aa90;font-size: 14px;text-align: center;font-family: Arial, sans-serif;border-collapse: collapse;" class="ui-sortable">                            </td>                        </tr>                        <tr>                            <td style="font-size: 12px;font-family: Arial, sans-serif;border-collapse: collapse;">                            </td>                        </tr>                    </tbody></table>                </td>            </tr>        </tbody></table>    </center></div></body></html>'

        asunto = "[dailyjob] Has recibido una invitación para unirte a un proyecto"

        # connection = notifications.get_connection("smtp.gmail.com", "todos.yeboyebo@gmail.com", "555zapato", "465", "SSL")Zv3-hZx4NB2eurm
        connection = notifications.get_connection("smtp.zoho.com", "soporte@dailyjob.io", "I7c5uXGnNuee", "465", "SSL")
        response = notifications.sendMail(connection, "Soporte dailyjob<soporte@dailyjob.io>", asunto, cuerpo, [email])

        if not response:
            return False
        return True

    def gesttare_checkProyectosFormDraw(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        if str(cursor.valueBuffer("idresponsable")) == str(usuario):
            return True
        is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        # id_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = ".format(str(usuario)))
        # if not is_superuser or id_company != cursor.valueBuffer("idproyecto"):
        if not is_superuser:
            return "hidden"
        return True

    def gesttare_checkResponsableDraw(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        if str(cursor.valueBuffer("idresponsable")) == str(usuario):
            return True
        is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        # id_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = ".format(str(usuario)))
        # if is_superuser and id_company == cursor.valueBuffer("idproyecto"):
        if is_superuser:
            return True
        return "hidden"

    def gesttare_checkDrawPorcentajeHito(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        if str(cursor.valueBuffer("idresponsable")) == str(usuario):
            return True
        is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        id_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = ".format(str(usuario)))
        if is_superuser and id_company == cursor.valueBuffer("idproyecto"):
            return True
        return "hidden"

    def gesttare_checkProyectosExterno(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        if str(cursor.valueBuffer("idresponsable")) == str(usuario):
            return True
        is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        id_company = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = ".format(str(usuario)))
        if is_superuser and id_company == cursor.valueBuffer("idproyecto"):
            return True
        return "disabled"

    def gesttare_commonCalculateField(self, fN=None, cursor=None):
        valor = None
        if fN == u"hdedicadas":
            valor = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"SUM(hdedicadas)", ustr(u"idproyecto = '", str(cursor.valueBuffer(u"idproyecto")), u"'")) or 0
            if isNaN(valor):
                valor = 0
            # valor = flgesttare_def.iface.time_to_seconds(valor)

        if fN == u"costetotal":
            valor = parseFloat(cursor.valueBuffer(u"costeinterno")) + parseFloat(cursor.valueBuffer(u"costeexterno"))
            if isNaN(valor):
                valor = 0
            valor = qsatype.FLUtil.roundFieldValue(valor, u"gt_proyectos", u"costetotal")

        if fN == u"costeinterno":
            valor = qsatype.FLUtil.sqlSelect(u"gt_tareas", u"SUM(coste)", ustr(u"idproyecto = '", str(cursor.valueBuffer(u"idproyecto")), u"'"))
            if isNaN(valor):
                valor = 0
            valor = qsatype.FLUtil.roundFieldValue(valor, u"gt_proyectos", u"costeinterno")

        if fN == u"rentabilidad":
            presupuesto = parseFloat(cursor.valueBuffer(u"presupuesto"))

            if isNaN(presupuesto):
                presupuesto = 0
            if presupuesto == 0:
                valor = 0
            else:
                valor = ((presupuesto - cursor.valueBuffer(u"costetotal")) * 100) / presupuesto

            if isNaN(valor):
                valor = 0
            valor = qsatype.FLUtil.roundFieldValue(valor, u"gt_proyectos", u"rentabilidad")
        return valor

    def gesttare_iniciaValoresCursor(self, cursor=None):
        usuario = qsatype.FLUtil.nameUser()
        hoy = qsatype.Date()
        fechacreacion = str(hoy)[:10]
        idcompany = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
        cursor.setValueBuffer(u"idcompany", idcompany)
        cursor.setValueBuffer("idresponsable", usuario)
        cursor.setValueBuffer("fechacreacion", fechacreacion)
        # qsatype.FactoriaModulos.get('formRecordgt_proyectos').iface.iniciaValoresCursor(cursor)
        return True

    def gesttare_archivar_proyecto(self, oParam, cursor):
        response = {}
        if "confirmacion" in oParam and oParam["confirmacion"]:
            usuario = qsatype.FLUtil.nameUser()
            is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
            id_company = qsatype.FLUtil.sqlSelect(u"aqn_user", u"idcompany", ustr(u"idusuario = '", str(usuario), u"'"))
            if str(cursor.valueBuffer("idresponsable")) == str(usuario) or (is_superuser and id_company == cursor.valueBuffer("idcompany")):
                cursor.setModeAccess(cursor.Edit)
                cursor.refreshBuffer()
                cursor.setValueBuffer("archivado", not cursor.valueBuffer("archivado"))
                if (cursor.valueBuffer("archivado")):
                    response["msg"] = "Proyecto archivado"
                else:
                    response["msg"] = "Proyecto abierto"
                if not cursor.commitBuffer():
                    return False
            else:
                response["status"] = 1
                response["msg"] = "No se puede archivar el proyecto"
                return response
        else:
            response['status'] = 2
            # response['resul'] = True
            if cursor.valueBuffer("archivado"):
                msg = "¿Seguro que quieres recuperar el proyecto?"
            else:
                msg = "¿Seguro que quieres archivar el proyecto?"
            response['confirm'] = msg
            return response
        return response

    def gesttare_borrar_proyecto(self, oParam, cursor):
        resul = {}
        if "confirmacion" in oParam and oParam["confirmacion"]:
            usuario = qsatype.FLUtil.nameUser()
            is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
            if str(cursor.valueBuffer("idresponsable")) == str(usuario) or is_superuser:
                cursor.setModeAccess(cursor.Del)
                cursor.refreshBuffer()
                if not cursor.commitBuffer():
                    return False    
            else:
                resul["status"] = 1
                resul["msg"] = "No se puede eliminar el proyecto"
                return resul

            resul["return_data"] = False
            resul["msg"] = "Proyecto y tareas asociadas eliminados correctamente"
        else:
            usuario = qsatype.FLUtil.nameUser()
            is_superuser = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
            if str(cursor.valueBuffer("idresponsable")) == str(usuario) or is_superuser:
                resul['status'] = 2
                resul['confirm'] = "¿Seguro que quieres eliminar el proyecto y todas sus tareas asociadas?"
            else:
                resul["status"] = 1
                resul["msg"] = "No se puede eliminar el proyecto"
                return resul
        return resul

    def gesttare_getRentabilidadGraphic(self, model, template):
        # resto = str("{:,.2f}".format(100 - model.rentabilidad).replace(".", ",")) + "%"
        # rentabilidad = str("{:,.2f}".format(model.rentabilidad).replace(".", ",")) + "%"
        # print("rentabilidad: ", rentabilidad)
        tengopermiso = flgesttare_def.iface.compruebaPermisosPlan("rentabilidad_proyecto")
        if tengopermiso != True:
            return tengopermiso

        return [{"type": "pieDonutChart", "data": [{"name": "Rentabilidad", "value": model.rentabilidad, "color": "#50d2ce"}, {"name": "Resto", "value": ("{0:.2f}".format(100 - model.rentabilidad)), "color": "#bababa"}], "innerText": True, "animate": True, "size": 90, "showInfo": False}]
        # return [
        #     {"type": "pieDonutChart", "data": [{"name": "Nombre", "value": 20, "color": "red"}, {"name": "Dos", "value": 80, "color": "orange"}], "innerText": True, "animate": True, "size": 90},
        #     {"type": "pieChart", "data": [{"name": "Nombre", "value": 20, "color": "red"}, {"name": "Dos", "value": 80, "color": "orange"}], "innerText": True, "animate": True},
        #     {"type": "horizontalBarChart", "data": [{"name": "Nombre", "value": 20, "color": "red"}, {"name": "Dos", "value": 80, "color": "orange"}], "innerText": True}]

    def gesttare_queryGrid_proyectosarchivados(self, model, filters):
        where = "gt_proyectos.archivado"
        usuario = qsatype.FLUtil.nameUser()
        # isadmin = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        # if not isadmin:
        where = where + " AND gt_particproyecto.idusuario = " + str(usuario)
        query = {}
        query["tablesList"] = ("gt_proyectos, gt_particproyecto")
        query["select"] = ("gt_proyectos.idproyecto, gt_proyectos.nombre, gt_proyectos.estado, gt_proyectos.fechainicio, gt_proyectos.fechaterminado, gt_proyectos.idcliente")
        query["from"] = ("gt_proyectos INNER JOIN gt_particproyecto ON gt_proyectos.idproyecto = gt_particproyecto.idproyecto")
        query["where"] = (where)
        query["groupby"] = ("gt_proyectos.idproyecto")
        return query

    def gesttare_queryGrid_rentabilidadProyectos(self, model, filters):
        where = "1 = 1"
        usuario = qsatype.FLUtil.nameUser()
        # isadmin = qsatype.FLUtil.sqlSelect(u"auth_user", u"is_superuser", ustr(u"username = '", str(usuario), u"'"))
        # if not isadmin:
        compania = qsatype.FLUtil.sqlSelect("aqn_user", "idcompany", "idusuario = " + str(usuario))
        if filters:
            if "[gt_proyectos.nombre]" in filters and filters["[gt_proyectos.nombre]"] != "":
                where += " AND UPPER(gt_proyectos.nombre) like '%{}%'".format(filters["[gt_proyectos.nombre]"].upper())
            if "[gt_proyectos.estado]" in filters and filters["[gt_proyectos.estado]"] != "":
                where += " AND gt_proyectos.estado = '{}'".format(filters["[gt_proyectos.estado]"])
            if "[cliente]" in filters and filters["[cliente]"] != "":
                where += " AND gt_proyectos.idcliente = '{}'".format(filters["[cliente]"])
            if "[d_gt_proyectos.fechainicio]" in filters and filters["[d_gt_proyectos.fechainicio]"] != "":
                where += " AND gt_proyectos.fechainicio >= '{}'".format(filters["[d_gt_proyectos.fechainicio]"])
            if "[h_gt_proyectos.fechainicio]" in filters and filters["[h_gt_proyectos.fechainicio]"] != "":
                where += " AND gt_proyectos.fechainicio <= '{}'".format(filters["[h_gt_proyectos.fechainicio]"])
            if "[d_gt_proyectos.fechaterminado]" in filters and filters["[d_gt_proyectos.fechaterminado]"] != "":
                where += " AND gt_proyectos.fechaterminado >= '{}'".format(filters["[d_gt_proyectos.fechaterminado]"])
            if "[h_gt_proyectos.fechaterminado]" in filters and filters["[h_gt_proyectos.fechaterminado]"] != "":
                where += " AND gt_proyectos.fechaterminado <= '{}'".format(filters["[h_gt_proyectos.fechaterminado]"])

            if "[buscador]" in filters and filters["[buscador]"] != "":
                where += " AND UPPER(gt_proyectos.nombre) LIKE '%{}%'".format(filters["[buscador]"].upper())

            if "[cb_gt_proyectos.archivado]" in filters and filters['[cb_gt_proyectos.archivado]'] == "Archivados":
                where += " AND gt_proyectos.archivado = true"
            elif "[cb_gt_proyectos.archivado]" in filters and filters['[cb_gt_proyectos.archivado]'] == "Todos":
                where += ""
            elif "[cb_gt_proyectos.archivado]" in filters and filters['[cb_gt_proyectos.archivado]'] == "" or ['[cb_gt_proyectos.archivado]'] in filters and filters['[cb_gt_proyectos.archivado]'] == "Activos":
                where += " AND gt_proyectos.archivado = false"
        else:
            where += " AND gt_proyectos.archivado = false"
        where += " AND gt_proyectos.idcompany = " + str(compania)
        query = {}
        query["tablesList"] = ("gt_proyectos")
        query["select"] = ("gt_proyectos.idproyecto, gt_proyectos.nombre, gt_proyectos.estado, gt_proyectos.idcliente, gt_proyectos.fechainicio, gt_proyectos.fechaterminado, gt_proyectos.presupuesto, gt_proyectos.costetotal, gt_proyectos.rentabilidad, (gt_proyectos.presupuesto - gt_proyectos.costetotal) as Resultado")
        query["from"] = ("gt_proyectos")
        query["where"] = (where)
        #query["groupby"] = ("gt_proyectos.idproyecto")
        return query

    def gesttare_iniciaValoresLabel(self, model=None, template=None, cursor=None, data=None):
        labels = {}
        if template == 'formRecord':
            hinvertidas = flgesttare_def.iface.seconds_to_time(cursor.valueBuffer("hdedicadas"), all_in_hours=True)
            hinvertidas = flgesttare_def.iface.formatearTotalTiempo(hinvertidas)
            if hinvertidas=="":
                hinvertidas = "00:00:00"
            labels["horasinvertidas"] = hinvertidas
            # labels["presupuestoFormat"] = str("{:,.2f}".format(cursor.valueBuffer("presupuesto")).replace(",", "@").replace(".", ",").replace("@", ".")) + " € "
            # labels["costeFormat"] = str("{:,.2f}".format(cursor.valueBuffer("costetotal")).replace(",", "@").replace(".", ",").replace("@", ".")) + " € "
            labels["presupuestoFormat"] = flgesttare_def.iface.formatearTotalPresupuesto(cursor.valueBuffer("presupuesto"))
            labels["costeFormat"] = flgesttare_def.iface.formatearTotalPresupuesto(cursor.valueBuffer("costetotal"))
        return labels

    def gesttare_vertareasproyecto(self, cursor):
        response = {}
        response["url"] = "/gesttare/gt_tareas/master"
        response["prefix"] = "gt_tareas"
        response["filter"] = '{"idproyecto": "' + str(cursor.valueBuffer("idproyecto")) + '"}'
        return response

    def gesttare_verTrackingProyecto(self, cursor):
        response = {}
        response["url"] = "/gesttare/gt_timetracking/master"
        response["prefix"] = "mastertimetracking"
        response["filter"] = '{"proyecto": "' + str(cursor.valueBuffer("idproyecto")) + '"}'
        return response

    def gesttare_gotoNuevoProyecto(self, model, oParam):
        user_name = qsatype.FLUtil.nameUser()
        #idc_diario = qsatype.FLUtil().quickSqlSelect("gt_proyectos", "idproyecto", "idusuario = '{}'".format(user_name))

        # idproyecto = "nuevoP2"
        # url = '/gesttare/gt_proyectos/newRecord?p_idproyecto=' + str(idproyecto) + '&p_idusuario=' + str(user_name)
        url='/gesttare/gt_proyectos/newRecord'
        resul = {}
        resul["url"] = url
        resul['status'] = 1
        return resul

    def gesttare_copiarProyecto(self, oParam, cursor):
        _i = self.iface
        response = {}
        if "confirmacion" in oParam and oParam["confirmacion"]:
            nombre = cursor.valueBuffer("nombre")
            if len(nombre) > 44:
                nombre = nombre[0:44]
            nombre = "Copia-" + nombre

            user_name = qsatype.FLUtil.nameUser()
            curCopia = qsatype.FLSqlCursor("gt_proyectos")
            curCopia.setModeAccess(curCopia.Insert)
            curCopia.refreshBuffer()
            # qsatype.FactoriaModulos.get('formRecordgt_proyectos').iface.iniciaValoresCursor(curCopia)
            self.iface.iniciaValoresCursor(curCopia)
            curCopia.setValueBuffer("idresponsable", user_name)
            curCopia.setValueBuffer("nombre", nombre)
            curCopia.setValueBuffer("descripcion", "")
            curCopia.setValueBuffer("imputable", False)
            curCopia.setValueBuffer("margenh", 0)
            curCopia.setValueBuffer("rentabilidad", 0)
            curCopia.setValueBuffer("rentabilidadsobre", 0)
            curCopia.setValueBuffer("archivado", False)
            curCopia.setValueBuffer("usaralbaranes", False)
            curCopia.setValueBuffer("desviacionh", 0)
            curCopia.setValueBuffer("costeinterno", 0)
            curCopia.setValueBuffer("costetotal", 0)
            curCopia.setValueBuffer("presupuesto", 0)
            curCopia.setValueBuffer("facturado", 0)
            curCopia.setValueBuffer("hestimadas", 0)
            curCopia.setValueBuffer("hdedicadas", 0)
            curCopia.setValueBuffer("hfacturadas", 0)
            curCopia.setValueBuffer("idcompany", cursor.valueBuffer("idcompany"))
            if not curCopia.commitBuffer():
                return False
            # if not qsatype.FLUtil.sqlInsert(u"gt_particproyecto", qsatype.Array([u"idusuario", u"idproyecto"]), qsatype.Array([idUsuario, curProyecto.valueBuffer(u"idproyecto")])):
            #         return False
            if not _i.copiarHitosProyecto(cursor, curCopia.valueBuffer("idproyecto")):
                return False
            response["url"] = "/gesttare/gt_proyectos/" + str(curCopia.valueBuffer("idproyecto"))
            return response
        response['status'] = 2
        msg = "Vas a copiar el proyecto con todos los hitos y tareas que contiene. No se copiaran datos de fechas, responsables, participantes, comentarios o registros de tiempo asociados a proyectos y tareas. \n ¿Quieres continuar?"
        response['confirm'] = msg
        return response

    def gesttare_copiarTareasHito(self, curHito, idproyecto, idhito):
        curTarea = qsatype.FLSqlCursor(u"gt_tareas")
        curTarea.select(ustr(u"idhito = '", curHito.valueBuffer("idhito"), u"'"))
        while curTarea.next():
            curTarea.setModeAccess(curTarea.Browse)
            curTarea.refreshBuffer()
            estado = curTarea.valueBuffer("codestado")
            curCopia = qsatype.FLSqlCursor("gt_tareas")
            curCopia.setModeAccess(curCopia.Insert)
            curCopia.refreshBuffer()
            curCopia.setValueBuffer("coste", 0)
            curCopia.setValueBuffer("hdedicadas", 0)
            curCopia.setValueBuffer("resuelta", False)
            curCopia.setValueBuffer("codestado", estado)
            curCopia.setValueBuffer("nombre", curTarea.valueBuffer("nombre"))
            curCopia.setValueBuffer("idproyecto", idproyecto)
            curCopia.setValueBuffer("idhito", idhito)
            if not curCopia.commitBuffer():
                return False
        # return False
        return True

    def gesttare_copiarHitosProyecto(self, cursor, idproyecto):
        _i = self.iface
        curHito = qsatype.FLSqlCursor(u"gt_hitosproyecto")
        curHito.select(ustr(u"idproyecto = '", str(cursor.valueBuffer("idproyecto")), u"'"))
        while curHito.next():
            curHito.setModeAccess(curHito.Browse)
            curHito.refreshBuffer()
            curCopia = qsatype.FLSqlCursor("gt_hitosproyecto")
            curCopia.setModeAccess(curCopia.Insert)
            curCopia.refreshBuffer()
            curCopia.setValueBuffer("resuelta", False)
            curCopia.setValueBuffer("nombre", curHito.valueBuffer("nombre"))
            curCopia.setValueBuffer("idproyecto", idproyecto)
            if not curCopia.commitBuffer():
                return False
            if not _i.copiarTareasHito(curHito, idproyecto, curCopia.valueBuffer("idhito")):
                return False
        return True

    def gesttare_validateCursor(self, cursor):
        msg = ""
        error = False
        if not cursor.valueBuffer("idresponsable"):
            msg += "Es necesario un responsable de proyecto <br/>"
            # qsatype.FLUtil.ponMsgError("Es necesario un responsable de proyecto <br/>")
            # return False
            error = True

        if cursor.modeAccess() == cursor.Insert:
            if not cursor.valueBuffer("fechaterminado"):
                msg += "El campo fecha fin no puede estar vacío"
                error = True

        if error:
            qsatype.FLUtil.ponMsgError(msg)
            return False
           
        return True

    def gesttare_gotoProyecto(self, model):
        url = '/gesttare/gt_proyectos/' + str(model.idproyecto) 
        return url

    def gesttare_drawif_archivado(self, cursor):
        # if cursor.valueBuffer("resuelta") == True:
        if cursor.valueBuffer("idproyecto"):
            archivado = qsatype.FLUtil.quickSqlSelect("gt_proyectos", "archivado", "archivado = '{}'".format(cursor.valueBuffer("archivado")))
            if archivado:
                return True
        return "hidden"

    def gesttare_invExterno(self, oParam, cursor):
        response = {}
        response['status'] = -1
        response['data'] = {}
        response["prefix"] = "gt_proyectos"
        response["title"] = "Invitación de usuarios externos"
        # response["confirm"] = "</br></br> ¿Quieres continuar?"
        response["serverAction"] = ""
        response["customButtons"] = [{"accion": "serverAction", "pk": cursor.valueBuffer("idproyecto"), "nombre": "Quiero que colabore", "serverAction": "actInvitarExternoColaborador", "className": "creaAnotacionButton"}, {"accion": "serverAction", "pk": cursor.valueBuffer("idproyecto"), "nombre": "Quiero que observe", "serverAction": "actInvitarExternoObservador", "className": "creaAnotacionButton"}]
        
        response['params'] = [
            {
                "tipo": 3,
                "verbose_name": "email",
                "key": "email",
                "validaciones": None,
                "select": True,
                "style": {
                    "width": "100%"
                }
            }
        ]
        
        return response


    def gesttare_actInvitarExternoColaborador(self, oParam, cursor):
        usuario = qsatype.FLUtil.nameUser()
        # print("param es ",oParam)
        # return True
        response = {}
        if not re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', oParam["email"].lower()):
            print("Correo incorrecto")
            response["status"] = 1
            response["msg"] = "Formato correo intorrecto"
            return response
        # usuario = qsatype.FLUtil.nameUser()
        curUsuario = qsatype.FLSqlCursor("aqn_user")
        curUsuario.select("email = '" + str(oParam["email"]) + "'")
        if not curUsuario.next():
            # response["status"] = 1
            # response["msg"] = "No existe usuario"
            # return response
            # codifica = oParam["email"] + str(cursor.valueBuffer("idproyecto"))
            # hashcode = hashlib.md5(codifica.encode('utf-8')).hexdigest()
            # curInvitacion = qsatype.FLSqlCursor(u"aqn_invitations")
            # curInvitacion.setModeAccess(curInvitacion.Insert)
            # curInvitacion.refreshBuffer()
            # curInvitacion.setValueBuffer(u"email", oParam["email"])
            # curInvitacion.setValueBuffer(u"hashcode", hashlib.md5(hashcode.encode('utf-8')).hexdigest())
            # # curInvitacion.setValueBuffer(u"idcompany", idcompany)
            # curInvitacion.setValueBuffer(u"idcompany", cursor.valueBuffer("idcompany"))
            # curInvitacion.setValueBuffer(u"idproyecto", cursor.valueBuffer("idproyecto"))
            # curInvitacion.setValueBuffer(u"fecha", str(qsatype.Date())[:10])
            # curInvitacion.setValueBuffer(u"activo", True)
            # curInvitacion.setValueBuffer(u"tipo", "colaborador")
            # curInvitacion.setValueBuffer(u"idusuarioorigen", usuario)
            # if not curInvitacion.commitBuffer():
            #     return False

            params = {
                "email": oParam["email"],
                "idproyecto": cursor.valueBuffer("idproyecto"),
                "idcompany": cursor.valueBuffer("idcompany"),
                "idusuarioorigen": usuario,
                "tipo": "colaborador"
            }
            APIQSA.entry_point('post', "aqn_invitations", usuario, params, "post")  
            # APIQSA.entry_point('post', "aqn_precompanies", usuario, params, "post")    
        else:
            curUsuario.setModeAccess(curUsuario.Browse)
            curUsuario.refreshBuffer()
            idcompany = curUsuario.valueBuffer("idcompany")
            # Comprobamos que no existe usuario con ese email para esa compañia
            if idcompany == cursor.valueBuffer("idcompany"):
                response["status"] = 1
                response["msg"] = "El usuario ya pertenece a la compañia"
                return response
            else:

                print("aqui enviamos la invitacion")
                codifica = oParam["email"] + str(cursor.valueBuffer("idproyecto"))
                hashcode = hashlib.md5(codifica.encode('utf-8')).hexdigest()
                curInvitacion = qsatype.FLSqlCursor(u"aqn_invitations")
                curInvitacion.setModeAccess(curInvitacion.Insert)
                curInvitacion.refreshBuffer()
                curInvitacion.setValueBuffer(u"email", oParam["email"])
                curInvitacion.setValueBuffer(u"hashcode", hashlib.md5(hashcode.encode('utf-8')).hexdigest())
                # curInvitacion.setValueBuffer(u"idcompany", idcompany)
                curInvitacion.setValueBuffer(u"idcompany", cursor.valueBuffer("idcompany"))
                curInvitacion.setValueBuffer(u"idproyecto", cursor.valueBuffer("idproyecto"))
                curInvitacion.setValueBuffer(u"fecha", str(qsatype.Date())[:10])
                curInvitacion.setValueBuffer(u"activo", True)
                curInvitacion.setValueBuffer(u"tipo", "colaborador")
                curInvitacion.setValueBuffer(u"idusuarioorigen", usuario)
                if not curInvitacion.commitBuffer():
                    return False
               
                id_destinatario =  qsatype.FLUtil.quickSqlSelect("aqn_user", "idusuario", "email = '{}'".format(oParam["email"]))
                curActualiz = qsatype.FLSqlCursor(u"gt_actualizaciones")
                curActualiz.setModeAccess(curActualiz.Insert)
                curActualiz.refreshBuffer()
                curActualiz.setValueBuffer(u"tipo", "colaborador")
                curActualiz.setValueBuffer(u"tipobjeto", "particproyectoE")
                curActualiz.setValueBuffer(u"otros", cursor.valueBuffer("nombre"))
                curActualiz.setValueBuffer(u"fecha", datetime.date.today())
                curActualiz.setValueBuffer(u"hora", time.strftime('%H:%M:%S'))
                curActualiz.setValueBuffer(u"idusuarioorigen", usuario)
                curActualiz.setValueBuffer(u"idobjeto", cursor.valueBuffer("idproyecto"))
                if not curActualiz.commitBuffer():
                    return False
                # _i = self.iface
                # if not _i.envioMailInvitacion(curInvitacion.valueBuffer("email"), cursor.valueBuffer("nombre"), curInvitacion.valueBuffer("hashcode"), curActualiz.valueBuffer("idactualizacion")):
                #     return False
                # if not qsatype.FLUtil.sqlInsert(u"gt_actualizaciones", qsatype.Array([u"tipo", u"tipobjeto", u"otros", "fecha", "hora", "idusuarioorigen"]), qsatype.Array(["colaborador", "particproyectoE", cursor.valueBuffer("nombre"), datetime.date.today(), time.strftime('%H:%M:%S'), usuario])):
                #     return False
                if not qsatype.FLUtil.sqlInsert(u"gt_actualizusuario", qsatype.Array([u"idactualizacion", u"idusuario", u"revisada"]), qsatype.Array([curActualiz.valueBuffer("idactualizacion"), id_destinatario, False])):
                    return False
                response["msg"] = "Invitación enviada correctamente"
                return response
                
        response = {}
        response["resul"] = True
        response["msg"] = "Invitación enviada correctamente"
        return response

    def gesttare_actInvitarExternoObservador(self, oParam, cursor):
        usuario = qsatype.FLUtil.nameUser()
        # print("param es ",oParam)
        # return True
        response = {}
        if not re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', oParam["email"].lower()):
            print("Correo incorrecto")
            response["status"] = 1
            response["msg"] = "Formato correo intorrecto"
            return response
        # usuario = qsatype.FLUtil.nameUser()
        curUsuario = qsatype.FLSqlCursor("aqn_user")
        curUsuario.select("email = '" + str(oParam["email"]) + "'")
        if not curUsuario.next():
            params = {
                "email": oParam["email"],
                "idproyecto": cursor.valueBuffer("idproyecto"),
                "idcompany": cursor.valueBuffer("idcompany"),
                "idusuarioorigen": usuario,
                "tipo": "observador"
            }
            APIQSA.entry_point('post', "aqn_invitations", usuario, params, "post")  
        else:
            curUsuario.setModeAccess(curUsuario.Browse)
            curUsuario.refreshBuffer()
            idcompany = curUsuario.valueBuffer("idcompany")
            # Comprobamos que no existe usuario con ese email para esa compañia
            if idcompany == cursor.valueBuffer("idcompany"):
                response["status"] = 1
                response["msg"] = "El usuario ya pertenece a la compañia"
                return response
            else:

                print("aqui enviamos la invitacion")
                codifica = oParam["email"] + str(cursor.valueBuffer("idproyecto"))
                hashcode = hashlib.md5(codifica.encode('utf-8')).hexdigest()
                curInvitacion = qsatype.FLSqlCursor(u"aqn_invitations")
                curInvitacion.setModeAccess(curInvitacion.Insert)
                curInvitacion.refreshBuffer()
                curInvitacion.setValueBuffer(u"email", oParam["email"])
                curInvitacion.setValueBuffer(u"hashcode", hashlib.md5(hashcode.encode('utf-8')).hexdigest())
                # curInvitacion.setValueBuffer(u"idcompany", idcompany)
                curInvitacion.setValueBuffer(u"idcompany", cursor.valueBuffer("idcompany"))
                curInvitacion.setValueBuffer(u"idproyecto", cursor.valueBuffer("idproyecto"))
                curInvitacion.setValueBuffer(u"fecha", str(qsatype.Date())[:10])
                curInvitacion.setValueBuffer(u"activo", True)
                curInvitacion.setValueBuffer(u"tipo", "observador")
                curInvitacion.setValueBuffer(u"idusuarioorigen", usuario)
                if not curInvitacion.commitBuffer():
                    return False
               
                id_destinatario =  qsatype.FLUtil.quickSqlSelect("aqn_user", "idusuario", "email = '{}'".format(oParam["email"]))
                curActualiz = qsatype.FLSqlCursor(u"gt_actualizaciones")
                curActualiz.setModeAccess(curActualiz.Insert)
                curActualiz.refreshBuffer()
                curActualiz.setValueBuffer(u"tipo", "observador")
                curActualiz.setValueBuffer(u"tipobjeto", "particproyectoE")
                curActualiz.setValueBuffer(u"otros", cursor.valueBuffer("nombre"))
                curActualiz.setValueBuffer(u"fecha", datetime.date.today())
                curActualiz.setValueBuffer(u"hora", time.strftime('%H:%M:%S'))
                curActualiz.setValueBuffer(u"idusuarioorigen", usuario)
                curActualiz.setValueBuffer(u"idobjeto", cursor.valueBuffer("idproyecto"))
                if not curActualiz.commitBuffer():
                    return False
                # _i = self.iface
                # if not _i.envioMailInvitacion(curInvitacion.valueBuffer("email"), cursor.valueBuffer("nombre"), curInvitacion.valueBuffer("hashcode"), curActualiz.valueBuffer("idactualizacion")):
                #     return False
                # if not qsatype.FLUtil.sqlInsert(u"gt_actualizaciones", qsatype.Array([u"tipo", u"tipobjeto", u"otros", "fecha", "hora", "idusuarioorigen"]), qsatype.Array(["colaborador", "particproyectoE", cursor.valueBuffer("nombre"), datetime.date.today(), time.strftime('%H:%M:%S'), usuario])):
                #     return False
                if not qsatype.FLUtil.sqlInsert(u"gt_actualizusuario", qsatype.Array([u"idactualizacion", u"idusuario", u"revisada"]), qsatype.Array([curActualiz.valueBuffer("idactualizacion"), id_destinatario, False])):
                    return False
                response["msg"] = "Invitación enviada correctamente"
                return response
                
        response = {}
        response["resul"] = True
        response["msg"] = "Invitación enviada correctamente"
        return response

    def __init__(self, context=None):
        super().__init__(context)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def field_nombreCliente(self, model):
        return self.ctx.gesttare_field_nombreCliente(model)

    def field_queryNombreCliente(self, model):
        return self.ctx.gesttare_field_queryNombreCliente(model)

    def iniciaValoresLabel(self, model=None, template=None, cursor=None, data=None):
        return self.ctx.gesttare_iniciaValoresLabel(model, template, cursor, data)

    def checkProyectosFormDraw(self, cursor):
        return self.ctx.gesttare_checkProyectosFormDraw(cursor)

    def checkResponsableDraw(self, cursor):
        return self.ctx.gesttare_checkResponsableDraw(cursor)

    def checkDrawPorcentajeHito(self, cursor):
        return self.ctx.gesttare_checkDrawPorcentajeHito(cursor)

    def checkProyectosExterno(self, cursor):
        return self.ctx.gesttare_checkProyectosExterno(cursor)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def actNuevoPartic(self, oParam, cursor):
        return self.ctx.gesttare_actNuevoPartic(oParam, cursor)

    def getFilters(self, model, name, template=None):
        return self.ctx.gesttare_getFilters(model, name, template)

    def check_permissions(self, model, prefix, pk, template, acl, accion=None):
        return self.ctx.gesttare_check_permissions(model, prefix, pk, template, acl, accion)

    def getProyectosUsuario(self, oParam):
        return self.ctx.gesttare_getProyectosUsuario(oParam)

    def dameEmailCreaTarea(self, oParam, cursor):
        return self.ctx.gesttare_dameEmailCreaTarea(oParam, cursor)

    def actInvitarExterno(self, oParam, cursor):
        return self.ctx.gesttare_actInvitarExterno(oParam, cursor)

    def actInvitarExternoColaborador(self, oParam, cursor):
        return self.ctx.gesttare_actInvitarExternoColaborador(oParam, cursor)

    def actInvitarExternoObservador(self, oParam, cursor):
        return self.ctx.gesttare_actInvitarExternoObservador(oParam, cursor)

    def invExterno(self, oParam, cursor):
        return self.ctx.gesttare_invExterno(oParam, cursor)

    def envioMailInvitacion(self, email, nombreProyecto, hashcode, invi):
        return self.ctx.gesttare_envioMailInvitacion(email, nombreProyecto, hashcode, invi)

    def commonCalculateField(self, fN, cursor):
        return self.ctx.gesttare_commonCalculateField(fN, cursor)

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.gesttare_iniciaValoresCursor(cursor)

    def archivar_proyecto(self, oParam, cursor):
        return self.ctx.gesttare_archivar_proyecto(oParam, cursor)

    def borrar_proyecto(self, oParam, cursor):
        return self.ctx.gesttare_borrar_proyecto(oParam, cursor)

    def getRentabilidadGraphic(self, model, template):
        return self.ctx.gesttare_getRentabilidadGraphic(model, template)

    def queryGrid_proyectosarchivados(self, model, filters):
        return self.ctx.gesttare_queryGrid_proyectosarchivados(model, filters)

    def queryGrid_rentabilidadProyectos(self, model, filters):
        return self.ctx.gesttare_queryGrid_rentabilidadProyectos(model, filters)

    def vertareasproyecto(self, cursor):
        return self.ctx.gesttare_vertareasproyecto(cursor)

    def verTrackingProyecto(self, cursor):
        return self.ctx.gesttare_verTrackingProyecto(cursor)

    def field_usuario(self, model):
        return self.ctx.gesttare_field_usuario(model)

    def color_nombre(self, model):
        return self.ctx.gesttare_color_nombre(model)

    def color_responsable(self, model):
        return self.ctx.gesttare_color_responsable(model)

    def color_fondo_estado(self, model):
        return self.ctx.gesttare_color_fondo_estado(model)

    def color_fondo_estado_query(self, model):
        return self.ctx.gesttare_color_fondo_estado_query(model)

    def color_fondo_resultado(self, model):
        return self.ctx.gesttare_color_fondo_resultado(model)

    def gotoNuevoProyecto(self, model, oParam):
        return self.ctx.gesttare_gotoNuevoProyecto(model, oParam)

    def copiarProyecto(self, oParam, cursor):
        return self.ctx.gesttare_copiarProyecto(oParam, cursor)

    def copiarTareasHito(self, cursor, idproyecto, idhito):
        return self.ctx.gesttare_copiarTareasHito(cursor, idproyecto, idhito)

    def copiarHitosProyecto(self, cursor, idproyecto):
        return self.ctx.gesttare_copiarHitosProyecto(cursor, idproyecto)

    def validateCursor(self, cursor):
        return self.ctx.gesttare_validateCursor(cursor)

    def gotoProyecto(self, model):
        return self.ctx.gesttare_gotoProyecto(model)

    def drawif_archivado(self, cursor):
        return self.ctx.gesttare_drawif_archivado(cursor)


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
