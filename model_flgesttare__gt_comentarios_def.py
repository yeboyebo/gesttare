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
        fields = [{'verbose_name': 'adjunto', 'func': 'field_adjunto'}, {'verbose_name': 'nombreUsuario', 'func': 'field_nombreUsuario'}]
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
