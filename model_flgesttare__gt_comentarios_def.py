# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration gesttare #
from YBLEGACY.constantes import *
from YBUTILS.APIQSA import APIQSA
from YBUTILS import gesDoc
import traceback
import sys


class gesttare(interna):

    def gesttare_getForeignFields(self, model, template=None):
        fields = []
        fields = [{'verbose_name': 'adjunto', 'func': 'field_adjunto'}, {'verbose_name': 'nombreUsuario', 'func': 'field_nombreUsuario'},{'verbose_name': 'observaIcon', 'func': 'field_observaIcon'},{'verbose_name': 'observaTitle', 'func': 'field_observaTitle'}]
        return fields

    def gesttare_getDesc(self):
        return None

    def gesttare_field_adjunto(self, model):
        nombre = None
        ficheros = gesDoc.getFiles("gt_comentarios", model.pk)
        idUsuario = qsatype.FLUtil.nameUser()
        # pk = model.pk
        # params = {
        #     'pk': pk,
        #     'prefix': "gt_comentarios"
        # }
        # # ficheros = APIQSA.entry_point('post', "gd_documentos", idUsuario, params, 'getFiles')
        # ficheros = APIQSA.entry_point('post', "gd_documentos", idUsuario, params, 'getFiles')
        adjuntos = []
        if ficheros:
            files = ""
            for file in ficheros:
                adjuntos.append({"id": file, "name": ficheros[file]["nombre"]})
            return adjuntos
            #     files = file + "./."
            # return files
        # if file:
        #     return file["nombre"]
        return nombre

    def gesttare_field_observaIcon(self, model):
        if model.publico:
            return "visibility_off"
        else:
            return "visibility"

        return ""

    def gesttare_field_observaTitle(self, model):
        if model.publico:
            return "Quitar comentario de público"
        else:
            return "Pasar comentario a público"
            
        return ""

    def gesttare_field_nombreUsuario(self, model):
        # nombre = qsatype.FLUtil.quickSqlSelect("aqn_user", "email", "idusuario = {}".format(model.idusuario.idusuario)) or ""
        nombre = "@" + model.idusuario.usuario
        return nombre

    def gesttare_check_permissions(self, model, prefix, pk, template, acl, accion):

        if accion == "delete":
            nombreUsuario = qsatype.FLUtil.nameUser()
            idUsuario = qsatype.FLUtil.sqlSelect("gt_comentarios","idusuario",str("idcomentario = {} AND idusuario = {}".format(pk, nombreUsuario)))
            # idcompanyProject = qsatype.FLUtil.sqlSelect(u"gt_proyectos", u"idcompany", ustr(u" idproyecto = '", pk, "'"))
            if not idUsuario:
                return False
        return True

    def gesttare_comentario_publico(self, model, oParam, cursor):
        user_name = qsatype.FLUtil.nameUser()
        msg = ""
        response = {}
       
        if not oParam or "confirmacion" not in oParam:
        
            response["status"] = 2
            response["confirm"] = "Vas a cambiar la visibilidad del comentario para observador. </br></br> ¿Quieres continuar?"
            response["serverAction"] = "comentario_publico"
          
            return response

        response["resul"] = True
       
        params = {
            "pk": cursor.valueBuffer("idcomentario")
        }
        APIQSA.entry_point('post', "gt_comentarios", user_name, params, "comentario_publico")
        publico = cursor.valueBuffer("publico")
        if not publico:
            msg = "Comentario visible para observador"
        else:
            msg = "Comentario no visible para observador"
        response["msg"] = msg

        return response

    def __init__(self, context=None):
        super().__init__(context)

    def getForeignFields(self, model, template=None):
        return self.ctx.gesttare_getForeignFields(model, template)

    def getDesc(self):
        return self.ctx.gesttare_getDesc()

    def field_adjunto(self, model):
        return self.ctx.gesttare_field_adjunto(model)

    def field_nombreUsuario(self, model):
        return self.ctx.gesttare_field_nombreUsuario(model)

    def check_permissions(self, model, prefix, pk, template, acl, accion=None):
        return self.ctx.gesttare_check_permissions(model, prefix, pk, template, acl, accion)

    def field_observaIcon(self, model):
        return self.ctx.gesttare_field_observaIcon(model)

    def field_observaTitle(self, model):
        return self.ctx.gesttare_field_observaTitle(model)

    def comentario_publico(self, model, oParam, cursor):
        return self.ctx.gesttare_comentario_publico(model, oParam, cursor)


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
