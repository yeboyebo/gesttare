# -*- coding: utf-8 -*-
import json
from YBLEGACY import qsatype
from django.http import HttpResponse
from rest_framework.response import Response
import hashlib
import json
from models.fllogin.aqn_user import aqn_user
from django.contrib.auth.models import User, Group


# @class_declaration interna_userlogin #
class interna_userlogin():
    pass


# @class_declaration users_login #
class users_login(interna_userlogin):

    @staticmethod
    def start(pk, data):
        if "usuario" not in data or "password" not in data:
            return HttpResponse("Faltan parametros", status=400)
        userpassword = qsatype.FLUtil.sqlSelect(u"aqn_user", u"password", u"email = '" + str(data["usuario"]) + u"'")
        if not userpassword:
            return HttpResponse("No existe el usuario", status=400)
        md5passwd = hashlib.md5(data["password"].encode('utf-8')).hexdigest()
        if userpassword != md5passwd:
            return HttpResponse("Contraseña incorrecta", status=400)

        return HttpResponse(json.dumps({"result": "true"}), status=200)


# @class_declaration create #
class get(users_login):
    pass
