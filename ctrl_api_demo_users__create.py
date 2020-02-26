# -*- coding: utf-8 -*-
import json
from YBLEGACY import qsatype
from django.http import HttpResponse
from rest_framework.response import Response

from models.flgesttare.gt_tareas import gt_tareas as tareas
from models.fllogin.aqn_user import aqn_user
import hashlib
from django.contrib.auth.models import User, Group


# @class_declaration interna_create #
class interna_create():
    pass


# @class_declaration diagnosis_create #
class diagnosis_create(interna_create):

    @staticmethod
    def start(pk, data):
        if "usuario" not in data or "email" not in data or "password" not in data or "nombre" not in data or "apellidos" not in data:
            return HttpResponse("Faltan parametros", status=400)
        md5passwd = hashlib.md5(data["password"].encode('utf-8')).hexdigest()
        username = diagnosis_create.checkUser(data["usuario"], 0)

        q = qsatype.FLSqlQuery()
        q.setTablesList(u"aqn_user")
        q.setSelect(u"activo, usuario")
        q.setFrom(u"aqn_user")
        q.setWhere(u"email = '" + data["email"] + "'")
        if not q.exec_():
            return HttpResponse("Error inesperado", status=400)

        if q.size() > 0:
            return HttpResponse("Usuario ya existe", status=400)

        cursor = qsatype.FLSqlCursor(u"aqn_user")
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer(u"password", md5passwd)
        cursor.setValueBuffer(u"usuario", username)
        cursor.setValueBuffer(u"nombre", data["nombre"])
        cursor.setValueBuffer(u"apellidos", data["apellidos"])
        cursor.setValueBuffer(u"email", data["email"])
        cursor.setValueBuffer(u"idcompany", 8)
        cursor.setValueBuffer(u"activo", True)
        if not cursor.commitBuffer():
            return HttpResponse("Error inesperado", status=400)
        user = User.objects.create_user(username=cursor.valueBuffer("idusuario"), password="ybllogin", first_name=username)
        user.save()
        
        return HttpResponse("Ok", status=200)

    @staticmethod
    def checkUser(usuario, iterance):
        existe = aqn_user.objects.filter(usuario__exact=usuario)
        if len(existe) >= 1:
            iterance = iterance + 1
            usuario = usuario + str(iterance)
            return diagnosis_create.checkUser(usuario, iterance)
        else:
            print("?????", usuario)
            return usuario

# @class_declaration create #
class create(diagnosis_create):
    pass
