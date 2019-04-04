# @class_declaration interna_aqn_user #
import importlib

from YBUTILS.viewREST import helpers

from YBLEGACY.FLUtil import FLUtil
from YBLEGACY import baseraw


class mtd_aqn_user(baseraw.RawModel):
    id = baseraw.AutoField(db_column="id", verbose_name=FLUtil.translate(u"Identificador", u"MetaData"), primary_key=True)._miextend(visiblegrid=False, OLDTIPO="SERIAL")
    password = baseraw.CharField(max_length=128)._miextend(OLDTIPO="STRING")
    last_login = baseraw.DateTimeField(blank=True, null=True)._miextend(OLDTIPO="DATE")
    usuario = baseraw.CharField(max_length=30)._miextend(OLDTIPO="STRING")
    nombre = baseraw.CharField(max_length=30)._miextend(OLDTIPO="STRING")
    apellidos = baseraw.CharField(max_length=30)._miextend(OLDTIPO="STRING")
    email = baseraw.CharField(unique=True, max_length=254)._miextend(OLDTIPO="STRING")
    idcompania = baseraw.ForeignKey("mtd_gt_companias", db_column="idcompania", verbose_name=FLUtil.translate(u"Compañia", u"MetaData"), blank=True, null=True, to_field="idcompania", on_delete=FLUtil.deleteCascade, related_name="aqn_user_idcompania__fk__gt_companias_idcompania")._miextend(visiblegrid=False, OLDTIPO="UINT")

    class Meta:
        abstract = True


class interna_aqn_user(mtd_aqn_user, helpers.MixinConAcciones):
    pass

    class Meta:
        abstract = True


# @class_declaration gesttare_aqn_user #
class gesttare_aqn_user(interna_aqn_user, helpers.MixinConAcciones):
    pass

    class Meta:
        abstract = True


# @class_declaration aqn_user #
class aqn_user(gesttare_aqn_user, helpers.MixinConAcciones):
    pass

    class Meta:
        managed = True
        verbose_name = "Usuarios"
        db_table = 'aqn_user'

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.fllogin.aqn_user_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
